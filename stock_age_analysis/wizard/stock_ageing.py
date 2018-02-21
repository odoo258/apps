# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from odoo.exceptions import UserError


def recursion_set_location_id(loc, code):
    if loc.name == code:
        return True
    if loc.location_id:
        return recursion_set_location_id(loc=loc.location_id, code=code)
    return False


class StockAgeAnalysis(models.AbstractModel):
    _name = 'report.stock_age_analysis.report_stock_age_analysis'

    @api.model
    def render_html(self, docids, data=None):
        company = data['form']['company_id'] and data['form']['company_id'][1] or False
        warehouse = data['form']['warehouse_id'] and data['form']['warehouse_id'][1] or False
        product_category = data['form']['product_category_id'] and data['form']['product_category_id'][1] or False
        product = data['form']['Product_id'] and data['form']['Product_id'][1] or False
        location = data['form']['location_id'][1]
        from_date = datetime.datetime.strptime(data['form']['from_date'], '%Y-%m-%d')
        days = data['form']['days']

        # get plant location from wizard
        if data['form'].get('location_id'):
            stock_location = self.env['stock.location'].search([('usage', '=', 'internal'),
                                                                ('id', '=', data['form']['location_id'][0])])
        else:
            stock_location = self.env['stock.location'].search([('usage', '=', 'internal')])

        # get excise group from wizard
        if data['form'].get('Product_id'):
            products = self.env['product.product'].search([('id', '=', data['form']['Product_id'][0])])
        elif data['form'].get('product_category_id'):
            products = self.env['product.product'].search([('categ_id', '=', data['form']['product_category_id'][0])])

        # import pdb;pdb.set_trace()
        final_list = []
        interval_list = []
        products_name = {}
        for i in range(5):
            new_date = from_date - datetime.timedelta(days=days)
            domain = [('in_date', '<=', from_date.strftime('%Y-%m-%d')),
                      ('location_id', 'in', stock_location.ids),
                      ('product_id', 'in', products.ids)
                      ]
            if i == 4:
                interval = '{}+'.format(days * i)
            else:
                interval = '{}-{}'.format(i * days, (i + 1) * days)
                domain.append(('in_date', '>', new_date.strftime('%Y-%m-%d')))
            interval_list.append(interval)
            stock_quants = self.env['stock.quant'].search(domain)
            for quant in stock_quants:
                if quant.product_id.id not in products_name:
                    products_name.update({quant.product_id.id: quant.product_id.name})
                for product_dict in final_list:
                    if quant.product_id.id in product_dict:
                        break
                else:
                    final_list.append({quant.product_id.id: []})

                for product_dict in final_list:
                    if quant.product_id.id in product_dict:
                        for small_dict in product_dict[quant.product_id.id]:
                            if small_dict['interval'] == interval:
                                small_dict['qty'] += quant.qty
                                break
                        else:
                            product_dict[quant.product_id.id].append({'interval': interval, 'qty': quant.qty})
                        break
            from_date = new_date
        for product_dict in final_list:
            for key, value in product_dict.iteritems():
                for gap in interval_list:
                    for small_dict in value:
                        if gap == small_dict['interval']:
                            break
                    else:
                        value.append({'interval': gap, 'qty': 0.0})
        print products_name
        import pdb;pdb.set_trace()
        docargs = {
            'doc_model': data['model'],
            'data': final_list,
            'company': company,
            'warehous': warehous,
            'location': location,
            'product_category': product_category,
            'product': product,
            'from_date': datetime.datetime.strptime(data['form']['from_date'], '%Y-%m-%d').date(),
            'days': days,
            'interval': interval_list,
            'name': products_name
        }
        return self.env['report'].render('stock_age_analysis.report_stock_age_analysis', docargs)


class stock_age_analysis(models.TransientModel):
    _name = "stock.ageing.wizard"
    _description = "Stock Age analysis wizard"

    company_id = fields.Many2one('res.company', 'Comapany')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    location_id = fields.Many2one('stock.location', 'Location', required=True)
    product_category_id = fields.Many2one('product.category', 'Product category')
    Product_id = fields.Many2one('product.product', 'Product')
    days = fields.Integer('Enter Period', default=30, required=True)
    from_date = fields.Date(required=True)

    @api.multi
    def print_report(self):
        if not self.product_category_id and not self.Product_id:
            raise UserError(_('Select one of Product category or Product'))
        data = {
            'ids': self.id,
            'model': 'stock.move',
            'form': self.read()[0]
        }
        stock_move = self.env['stock.move'].browse()
        return self.env['report'].get_action(stock_move, 'stock_age_analysis.report_stock_age_analysis', data=data)

    @api.onchange('company_id')
    def set_warehouse_id(self):
        self.warehouse_id = None
        if self.company_id:
            return {'domain': {'warehouse_id': [('company_id', '=', self.company_id.id)]}}
        return {'domain': {'warehouse_id': []}}

    @api.onchange('warehouse_id')
    def set_location_id(self):
        self.location_id = None
        if self.warehouse_id:
            location_ids = []
            locations = self.env['stock.location'].sudo().search([])
            for loc in locations:
                if loc.name == self.warehouse_id.code:
                    location_ids.append(loc.id)
                elif loc.location_id:
                    if recursion_set_location_id(loc=loc.location_id, code=self.warehouse_id.code):
                        location_ids.append(loc.id)
            return {'domain': {'location_id': [('id', 'in', location_ids)]}}
        return {'domain': {'location_id': []}}

    @api.onchange('product_category_id')
    def set_product_id(self):
        self.Product_id = None
        if self.product_category_id:
            return {'domain': {'Product_id': [('categ_id', '=', self.product_category_id.id)]}}
        return {'domain': {'Product_id': []}}
