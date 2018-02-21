# -*- coding: utf-8 -*-

from odoo import api, fields, models
import time
from datetime import datetime


class Interest(models.Model):
    _inherit = 'account.invoice'

    is_due_date = fields.Boolean(compute='_find_overdue_date')
    interest = fields.Float(readonly=True)

    @api.one
    def _find_overdue_date(self):
        if self.date_due <= time.strftime('%Y-%m-%d'):
            self.is_due_date = True

    @api.one
    def compute_interest(self):
        if self.residual > 0:
            fmt = '%Y-%m-%d'
            d1 = datetime.strptime(time.strftime('%Y-%m-%d'), fmt)
            d2 = datetime.strptime(self.date_due, fmt)
            daysDiff = abs((d2 - d1).days)
            R = self.payment_term_id.interest_rate
            self.residual -= self.interest
            self.amount_total -= self.interest
            if self.payment_term_id.interest_type == 'daily':
                self.interest = (self.residual * (R) *
                                 (float(daysDiff) / 365)) / 100
            if self.payment_term_id.interest_type == 'monthly':
                self.interest = (self.residual *(float(R) / 12) * (float(daysDiff) / 365)) / 100
            self.amount_total += self.interest
            # import pdb;pdb.set_trace()
            self.residual += self.interest

    @api.one
    def reset(self):
        self.amount_total = self.amount_untaxed + self.amount_tax
        self.residual -= self.interest
        self.interest = 0


class PaymentTerms(models.Model):
    _inherit = 'account.payment.term'

    interest_rate = fields.Integer(string="Interest Rate")
    interest_type = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ], string='Interest Type')
    account = fields.Many2one('account.account', string="Account")

class Cash_register(models.Model):
    _inherit = "account.payment"

    @api.multi
    def post(self):
        res = super(Cash_register, self).post()
        print self.invoice_ids.residual
        self.invoice_ids.residual = self.invoice_ids.amount_total - self.amount

# # -*- coding: utf-8 -*-

# from odoo import api, fields, models
# import time
# from datetime import datetime


# class Interest(models.Model):
#     _inherit = 'account.invoice'

#     is_due_date = fields.Boolean(compute='_find_overdue_date')
#     interest = fields.Float()

#     @api.one
#     def _find_overdue_date(self):
#         if self.date_due <= time.strftime('%Y-%m-%d'):
#             self.is_due_date = True

#     @api.one
#     def compute_interest(self):
#         fmt = '%Y-%m-%d'
#         d1 = datetime.strptime(time.strftime('%Y-%m-%d'), fmt)
#         d2 = datetime.strptime(self.date_due, fmt)
#         daysDiff = str((d1 - d2).days + 1)
#         R = self.payment_term_id.interest_rate
#         self.amount_total -= self.interest
#         if self.payment_term_id.interest_type == 'daily':
#             self.interest = (self.amount_total * (R) *
#                              (float(daysDiff) / 365)) / 100
#         if self.payment_term_id.interest_type == 'monthly':
#             self.interest = (self.amount_total * (float(R) / 12)
#                              * (float(daysDiff) / 365)) / 100
#         self.amount_total += self.interest
#         self.residual = self.amount_total

#     @api.one
#     def reset(self):
#         self.amount_total = self.amount_untaxed - self.amount_tax
#         self.residual = self.amount_total
#         self.interest = 0


# class PaymentTerms(models.Model):
#     _inherit = 'account.payment.term'

#     interest_rate = fields.Integer(string="Interest Rate")
#     interest_type = fields.Selection([
#         ('daily', 'Daily'),
#         ('monthly', 'Monthly'),
#     ], string='Interest Type')
#     account = fields.Many2one('account.account', string="Account")


# ------------------------------
 # @api.one
    # def compute_interest(self):
    #     fmt = '%Y-%m-%d'
    #     d1 = datetime.strptime(time.strftime('%Y-%m-%d'), fmt)
    #     d2 = datetime.strptime(self.date_due, fmt)
    #     daysDiff = str((d1 - d2).days + 1)
    #     R = self.payment_term_id.interest_rate
    #     self.residual-=self.interest
    #     self.amount_total -= self.interest
    #     if self.payment_term_id.interest_type == 'daily':
    #         self.interest = (self.amount_total * (R) *
    #                          (float(daysDiff) / 365)) / 100
    #     if self.payment_term_id.interest_type == 'monthly':
    #         self.interest = (self.amount_total * (float(R) / 12)
    #                          * (float(daysDiff) / 365)) / 100
    #     self.amount_total += self.interest
    #     self.residual += self.interest

    # @api.one
    # def reset(self):
    #     self.amount_total = self.amount_untaxed + self.amount_tax
    #     self.residual -=self.interest
    #     self.interest = 0
