# -*- coding: utf-8 -*-

import time
from odoo import api, models


class ReportFinancial(models.AbstractModel):
    _name = 'report.account_tax_report_drc.report_tax'

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        # report_lines = self.get_account_lines(data.get('form'))

        account_invoice = self.env['account.invoice'].search([])
        # import pdb
        # pdb.set_trace()

        # if selectopn_field data :
        #     taxes = ['IGST', 'GST']
        # if account_invoice.tax_line_ids:
        #     for bill in account_invoice.tax_line_ids:
        # bill.name

        # report_lines = self.get_account_lines(data.get('form'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            # 'get_account_lines': report_lines,
        }
        return self.env['report'].render('account_tax_report_drc.report_tax', docargs)
