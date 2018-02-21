# -*- coding: utf-8 -*-
import math
from collections import OrderedDict
from odoo.exceptions import UserError
from odoo import models, api, fields, _


def ean_checksum(eancode):
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    total = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    if not eancode:
        return False
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False

    return ean_checksum(eancode) == int(eancode[-1])


class barcodeLabelWizard(models.TransientModel):
    _name = "product.access.barcode.label"

    height = fields.Float("Label Height(px)", default=400.00)
    width = fields.Float("Label Width(px)", default=400.00)
    currency = fields.Many2one("res.currency", string="Currency")
    currency_position = fields.Selection([('after', 'after'), ('before', 'before')], default="after", string="Symbol position")
    barcode_type = fields.Selection([('Code128', 'Code128'), ('EAN13', 'EAN13')], default="EAN13")
    barcode_height = fields.Float("Display Height(px)", default=100.00)
    barcode_width = fields.Float("Display Width(px)", default=300.00)
    products = fields.One2many('products.lines', 'access_id')
    attributes = fields.One2many('products.fields', 'access_field')

    @api.model
    def default_get(self, fields):
        data = super(barcodeLabelWizard, self).default_get(fields)
        active_ids = self._context['active_ids']
        active_products = self.env['product.product'].browse(active_ids)

        current_field = []
        for product in active_products:
            wiz_vals = {
                'product_id': product.id,
                'product_qty': 1,
            }
            current_field.append((0, 0, wiz_vals))
        data['products'] = current_field
        return data

    @api.multi
    def get_report(self):
        if self._context is None:
            self._context = {}
        data = self.read()[0]
        data_dict = {}
        fields_dict = {}
        active_ids = self._context['active_ids']
        products_line_id = data['products']

        # Product repetition dictionary
        products_lines = self.env['products.lines'].browse(products_line_id)
        qty_dict = {}
        for line in products_lines:
            qty_dict.update({line.product_id.name: line.product_qty})

        # data dictionary of products and Fields
        active_products = self.env['products.lines'].browse(products_line_id).mapped('product_id')
        for product in active_products:
            product_temp = {}
            fields_dict = {}
            for field in self.attributes:
                temp = field.field_name.name
                fields_dict.update({str(field.field_name.name): {'value': product.read([temp])[0][temp],
                                                        'font_size': field.font_size,
                                                        'font_color': field.font_color,
                                                        'sequence': field.sequence,
                                                        'type': field.field_name.ttype
                                                            }})

                product_temp.update(fields_dict)
            data_dict.update({str(product.name): product_temp})

        data = {
                     'ids': active_ids,
                     'model': 'product.product',
                     'form': data,
                     'docs': data_dict,
                     'qty_dict': qty_dict
        }
        return self.env['report'].get_action(self, 'access_barcode_label.report_barcode', data)

class productsLines(models.TransientModel):
    _name = "products.lines"

    product_id = fields.Many2one('product.product', string="Products")
    product_qty = fields.Integer(string="Quantity")
    access_id = fields.Many2one('product.access.barcode.label')

class productFields(models.TransientModel):
    _name = "products.fields"

    font_size = fields.Float(default=30.00)
    font_color = fields.Selection([('red', 'red'), ('blue', 'blue'), ('yellow', 'yellow'),
                                    ('green', 'green'), ('black', 'black'),
                                    ('brown', 'brown'), ('white', 'white'),
                                    ('indigo', 'indigo'), ('grey', 'grey')],
                                    default='black')
    sequence = fields.Integer()
    field_name = fields.Many2one('ir.model.fields', domain="[('model_id', '=','Product')]", required=True)
    access_field = fields.Many2one('product.access.barcode.label')


class ParticularReport(models.AbstractModel):
    _name = 'report.access_barcode_label.report_barcode'

    @api.multi
    def render_html(self, docids, data=None):
        data_dict = data['docs']
        sequence_list = []

        # Width and Height
        label_width = data['form']['width']
        label_height = data['form']['height']
        barcode_width = data['form']['barcode_width']
        barcode_height = data['form']['barcode_height']

        if (label_width * 80) / 100 < barcode_width:
            raise UserError(_('Please keep Label\'s WIDTH atleast 80% greater than Barcode\'s WIDTH \n and also cosider extra fields that you are adding'))
        if (label_height * 80) / 100 < barcode_height:
            raise UserError(_('Please keep Label\'s HEIGHT atleast 80% greater than Barcode\'s HEIGHT \n and also cosider extra fields that you are adding'))

        # ORDERED DICTIONARY
        for k, v in data_dict.iteritems():
            for key, value in v.iteritems():
                sequence_list.append(value['sequence'])
            break
        sequence_list.sort()
        main_dict = OrderedDict()

        for k, v in data_dict.iteritems():
            sort_dict = {}
            sort_dict = OrderedDict()
            for num in sequence_list:
                for key, value in v.iteritems():
                    if value['type'] == 'many2one' and len(value['value']) == 2:
                        value['value'] = value['value'][1]
                    if num == value['sequence']:
                        sort_dict.update({key: value})
                    if key == 'ean13' and data['form']['barcode_type'] == 'EAN13':
                        if not check_ean(value['value']):
                            raise UserError(_(k + ' ' + 'product don\'t have valid "EAN13 Barcode" reference. \n Please enter valid EAN13 barcode'))
            main_dict.update({k: sort_dict})

        self.model = self.env.context.get('active_model')

        #  CURRENCY SYMBOL
        if data['form']['currency']:
            currency_symbol = self.env['res.currency'].browse(data['form']['currency'][0]).symbol
        else:
            currency_symbol = ""
        print data['form'],"kkkkkkkkkk"
        print currency_symbol
        print data['qty_dict']
        print self
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': self,
            'data': main_dict,
            'form': data['form'],
            'symbol': currency_symbol,
            'quantity': data['qty_dict'],
        }
        return self.env['report'].render('access_barcode_label.report_barcode', docargs)
