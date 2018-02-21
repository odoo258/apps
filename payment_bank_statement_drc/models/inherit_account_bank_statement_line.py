# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Bank(models.Model):
    _inherit = 'account.bank.statement.line'

    memo = fields.Char(string='Memo')


class Bank_reg(models.Model):
    _inherit = "account.payment"

    bank_reg_entry = fields.Boolean(string='Bank Register Entry')
    bank_reg = fields.Many2one('account.bank.statement', domain="[('journal_type','=','bank')]", 
                              string="Bank Register")
   
    @api.multi
    def post(self):
        res = super(Bank_reg, self).post()
        aml_obj = self.env['account.payment'].with_context(check_move_validity=False)
        bank_record = self.env['account.bank.statement'].search([('name', '=', self.bank_reg.name)])
        first_line_dict = {
           'partner_id': self.partner_id,
           'name': self.name,
           'ref': self.name,
           'date': self.payment_date,
           'memo': self.communication,
           'amount': self.amount,
        }
        bank_record.line_ids = [(0, 0, first_line_dict)]
        return res
