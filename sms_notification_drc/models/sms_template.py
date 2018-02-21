# -*- coding: utf-8 -*-
from odoo import fields, models


class TemplateSms(models.Model):
    _name = "template.sms"
    _rec_name = 'template_name'

    template_name = fields.Char(string="Name", required=True)
    template_global = fields.Boolean(string="Global")
    template_condition = fields.Selection([('order_place', 'Order Place'), ('order_confirm', 'Order Confirm'), (
        'order_delivered', 'Order Delivered')])
    template_model_id = fields.Many2one(
        'ir.model', string="Applies to", domain=[('model', '=', 'sale.order')])
    template_auto_delete = fields.Boolean(string="Auto Delete")
    content = fields.Text()
