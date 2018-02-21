# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class BankStatement(models.Model):
    _inherit = 'account.bank.statement.line'

    memo = fields.Char(string='Memo')


class Cash_register(models.Model):
    _inherit = "account.payment"

    cash_reg_entry = fields.Boolean(string='Cash Register Entry')
    cash_reg = fields.Many2one('account.bank.statement', domain="[('journal_type','=','cash')]",
                               string="Cash Register", required=True)

    @api.multi
    def post(self):
        res = super(Cash_register, self).post()
        cash_record = self.env['account.bank.statement'].search(
            [('name', '=', self.cash_reg.name)])
        first_line_dict = {
            'partner_id': self.partner_id,
            'name': self.name,
            'ref': self.name,
            'date': self.payment_date,
            'memo': self.communication,
            'amount': self.amount,
        }
        cash_record.line_ids = [(0, 0, first_line_dict)]
        return res
