# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('to_approve', 'To Approve'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.multi
    def check_validation(self):
        for order in self:
            if order.company_id.so_double_validation == 'one_step'\
                    or (order.company_id.so_double_validation == 'two_step' and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.so_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('sales_team.group_sale_manager'):
                order.action_confirm()
            else:
                order.write({'state': 'to_approve'})
        return True

    @api.multi
    def second_approval(self):
        for order in self:
            order.action_confirm()
        return True