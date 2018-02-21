# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
import time
from odoo import api, fields, models, _
# saleorders=None
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class AccountCoomonReport(models.TransientModel):
    _inherit = "account.common.report"
    # _name = "account.report.partner.ledger1"

    @api.model
    def _get_partner(self):
        res_obj = self._context.get('active_id')
        print res_obj,":::::::::::::::::12"
        return res_obj

    result_selection = fields.Selection([('customer', 'Receivable Accounts'),
                                         ('supplier', 'Payable Accounts'),
                                         ('customer_supplier',
                                          'Receivable and Payable Accounts')
                                         ], string="Partner's", required=True, default='customer')
    res = fields.Many2one('res.partner',default=_get_partner,string="LOL")
    amount_currency = fields.Boolean(
        "With Currency", help="It adds the currency column on report if the currency differs from the company currency.")
    reconciled = fields.Boolean('Reconciled Entries')
    

    def _print_report(self,data):
        # res = self._context('active_id')
        print self.res,":::::::::::::::::;"
        data['form'].update({'reconciled': self.reconciled,
                             'amount_currency': self.amount_currency})
        return self.env['report'].get_action(self.res, 'account.report_partnerledger', data=data)

    # def _print_report(self, data):
    #     # data = self.pre_print_report(data)
    #     data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency})
    # return self.env['report'].get_action(self,
    # 'account.report_partnerledger', data=data)


# class ReportPartnerLedger(models.AbstractModel):
#     _name = 'report.account_customer_statement.report_partnerledger1'
#     _inherit = 'report.account.report_partnerledger'


#     @api.model
#     def render_html(self, docids, data=None):
        # if True:
        #     return self.env['report'].render('account_customer_statement.report_partnerledger1', docids)
        # return super(ReportPartnerLedger,self).render_html(docids,data)
    # def _lines(self, data, partner):
    #     full_account = []
    #     currency = self.env['res.currency']
    #     query_get_data = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
    #     reconcile_clause = "" if data['form']['reconciled'] else ' AND "account_move_line".reconciled = false '
    #     params = [partner.id, tuple(data['computed']['move_state']), tuple(data['computed']['account_ids'])] + query_get_data[2]
    #     query = """
    #         SELECT "account_move_line".id, "account_move_line".date, j.code, acc.code as a_code, acc.name as a_name, "account_move_line".ref, m.name as move_name, "account_move_line".name, "account_move_line".debit, "account_move_line".credit, "account_move_line".amount_currency,"account_move_line".currency_id, c.symbol AS currency_code
    #         FROM """ + query_get_data[0] + """
    #         LEFT JOIN account_journal j ON ("account_move_line".journal_id = j.id)
    #         LEFT JOIN account_account acc ON ("account_move_line".account_id = acc.id)
    #         LEFT JOIN res_currency c ON ("account_move_line".currency_id=c.id)
    #         LEFT JOIN account_move m ON (m.id="account_move_line".move_id)
    #         WHERE "account_move_line".partner_id = %s
    #             AND m.state IN %s
    #             AND "account_move_line".account_id IN %s AND """ + query_get_data[1] + reconcile_clause + """
    #             ORDER BY "account_move_line".date"""
    #     self.env.cr.execute(query, tuple(params))
    #     res = self.env.cr.dictfetchall()
    #     sum = 0.0
    #     lang_code = self.env.context.get('lang') or 'en_US'
    #     lang = self.env['res.lang']
    #     lang_id = lang._lang_get(lang_code)
    #     date_format = lang_id.date_format
    #     for r in res:
    #         r['date'] = datetime.strptime(r['date'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
    #         r['displayed_name'] = '-'.join(
    #             r[field_name] for field_name in ('move_name', 'ref', 'name')
    #             if r[field_name] not in (None, '', '/')
    #         )
    #         sum += r['debit'] - r['credit']
    #         r['progress'] = sum
    #         r['currency_id'] = currency.browse(r.get('currency_id'))
    #         full_account.append(r)
    #     return full_account

    # def _sum_partner(self, data, partner, field):
    #     if field not in ['debit', 'credit', 'debit - credit']:
    #         return
    #     result = 0.0
    #     query_get_data = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
    #     reconcile_clause = "" if data['form']['reconciled'] else ' AND "account_move_line".reconciled = false '

    #     params = [partner.id, tuple(data['computed']['move_state']), tuple(data['computed']['account_ids'])] + query_get_data[2]
    #     query = """SELECT sum(""" + field + """)
    #             FROM """ + query_get_data[0] + """, account_move AS m
    #             WHERE "account_move_line".partner_id = %s
    #                 AND m.id = "account_move_line".move_id
    #                 AND m.state IN %s
    #                 AND account_id IN %s
    #                 AND """ + query_get_data[1] + reconcile_clause
    #     self.env.cr.execute(query, tuple(params))

    #     contemp = self.env.cr.fetchone()
    #     if contemp is not None:
    #         result = contemp[0] or 0.0
    #     return result

    # @api.model
    # def render_html(self, docids, data=None):
    #     data['computed'] = {}

    #     obj_partner = self.env['res.partner']
    #     query_get_data = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
    #     data['computed']['move_state'] = ['draft', 'posted']
    #     if data['form'].get('target_move', 'all') == 'posted':
    #         data['computed']['move_state'] = ['posted']
    #     result_selection = data['form'].get('result_selection', 'customer')
    #     if result_selection == 'supplier':
    #         data['computed']['ACCOUNT_TYPE'] = ['payable']
    #     elif result_selection == 'customer':
    #         data['computed']['ACCOUNT_TYPE'] = ['receivable']
    #     else:
    #         data['computed']['ACCOUNT_TYPE'] = ['payable', 'receivable']

    #     self.env.cr.execute("""
    #         SELECT a.id
    #         FROM account_account a
    #         WHERE a.internal_type IN %s
    #         AND NOT a.deprecated""", (tuple(data['computed']['ACCOUNT_TYPE']),))
    #     data['computed']['account_ids'] = [a for (a,) in self.env.cr.fetchall()]
    #     params = [tuple(data['computed']['move_state']), tuple(data['computed']['account_ids'])] + query_get_data[2]
    #     reconcile_clause = "" if data['form']['reconciled'] else ' AND "account_move_line".reconciled = false '
    #     query = """
    #         SELECT DISTINCT "account_move_line".partner_id
    #         FROM """ + query_get_data[0] + """, account_account AS account, account_move AS am
    #         WHERE "account_move_line".partner_id IS NOT NULL
    #             AND "account_move_line".account_id = account.id
    #             AND am.id = "account_move_line".move_id
    #             AND am.state IN %s
    #             AND "account_move_line".account_id IN %s
    #             AND NOT account.deprecated
    #             AND """ + query_get_data[1] + reconcile_clause
    #     self.env.cr.execute(query, tuple(params))
    #     partner_ids = [res['partner_id'] for res in self.env.cr.dictfetchall()]
    #     partners = obj_partner.browse(partner_ids)
    #     partners = sorted(partners, key=lambda x: (x.ref, x.name))

    #     docargs = {
    #         'doc_ids': partner_ids,
    #         'doc_model': self.env['res.partner'],
    #         'data': data,
    #         'docs': partners,
    #         'time': time,
    #         'lines': self._lines,
    #         'sum_partner': self._sum_partner,
    #     }
    #     return self.env['report'].render('account_customer_statement.report_partnerledger1', docargs)
