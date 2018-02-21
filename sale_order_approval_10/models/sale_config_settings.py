# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = "sale.config.settings"

    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *")
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount', string="Double validation amount *", currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True,
                                          help='Utility field to express amount currency')
