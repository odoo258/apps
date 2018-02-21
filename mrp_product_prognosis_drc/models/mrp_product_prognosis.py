# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MrpConfig(models.TransientModel):
    _inherit = 'mrp.config.settings'

    allow_boolean = fields.Boolean(
        string="Do not calc consumables in MRP potential")

    @api.model
    def get_default_allow_boolean(self, fields):
        return {
            'allow_boolean': self.env['ir.values'].get_default('mrp.config.settings', 'allow_boolean')
        }

    @api.multi
    def set_default_allow_boolean(self):
        IrValues = self.env['ir.values']
        IrValues = IrValues.sudo()
        IrValues.set_default(
            'mrp.config.settings', 'allow_boolean', self.allow_boolean)


class ProducttTemplate(models.Model):
    _inherit = 'product.template'

    mrp_potential = fields.Integer(
        string="MRP Potential", compute='_compute_product_detail')
    bottleneck_component = fields.Many2many(
        'product.product', string="Bottleneck Component", compute='_compute_product_detail')
    mrp_forecast = fields.Integer(
        string="MRP Potential forecast", compute='_compute_product_detail')

    @api.one
    def _compute_product_detail(self):
        """Returns mrp potential,mrp forecast and borrleneck component of products"""
        bills = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.id)])
        for bom in bills:
            available, forecast, product_detail, potential, bottleneck, quantity, bottleneck_component = [
            ], [], [], [], [], [], []
            for bom_line in bom.bom_line_ids:
                if bom_line.product_qty * bom_line.product_id.qty_available >= bom_line.product_id.qty_available:
                    quantity.append(
                        (bom_line.product_id.qty_available / bom_line.product_qty))
                    bottleneck.append({
                        'product_id': bom_line.product_id,
                        'value': bom_line.product_id.qty_available / bom_line.product_qty,
                    })
                product = self.env['mrp.bom'].search(
                    [('product_tmpl_id', '=', bom_line.product_id.name)])
                if product:
                    for record in product.bom_line_ids:
                        if {
                                'model': bom.product_tmpl_id,
                                'product': product.product_tmpl_id,
                                'quantity': record.product_id.qty_available / record.product_qty} not in product_detail:
                            product_detail.append({
                                'model': bom.product_tmpl_id,
                                'product': product.product_tmpl_id,
                                'quantity': record.product_id.qty_available / record.product_qty})
                available.append(
                    int(bom_line.product_id.qty_available / bom_line.product_qty))
                forecast.append(
                    int(bom_line.product_id.virtual_available / bom_line.product_qty))
                self.mrp_potential = min(available) > 0 and min(
                    available) or 0
                self.mrp_forecast = min(forecast) > 0 and min(forecast) or 0
            for record in product_detail:
                lead = self.env['product.template'].browse(
                    record['model'])
                for i in record['model']:
                    potential.append(record['quantity'])
            if len(potential) > 0:
                self.mrp_potential += min(potential)
            for record in bottleneck:
                if record['value'] == 0.0:
                    bottleneck_component.append(record['product_id'].id)
                    self.bottleneck_component = bottleneck_component
                elif len(set(quantity)) == 1:
                    # print len(set(quantity))
                    pass
                elif int(min(quantity)) > 0.0:
                    self.bottleneck_component = record['product_id']
