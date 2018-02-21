# -*- coding: utf-8 -*-
import time
import datetime
from odoo import api, models


class ReportTaxReport(models.AbstractModel):
    _name = 'report.tax_report.report_tax_report'

    @api.multi
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        data['form']['date_from'] = datetime.datetime.strptime(data['form']['date_from'], '%Y-%m-%d').strftime('%d-%m-%Y')
        data['form']['date_to'] = datetime.datetime.strptime(data['form']['date_to'], '%Y-%m-%d').strftime('%d-%m-%Y')
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'move_lines': data['paid_lines'],
            'received_move_lines': data['received_lines'],
            'grand_base': data['paid_grand_base'],
            'grand_tax': data['paid_grand_tax'],
            'received_grand_base': data['received_grand_base'],
            'received_grand_tax': data['received_grand_tax'],
            'grand_base_total': data['paid_grand_base'] + data['received_grand_base'],
            'grand_tax_total': data['paid_grand_tax'] + data['received_grand_tax']
        }
        return self.env['report'].render('tax_report.report_tax_report', docargs)
