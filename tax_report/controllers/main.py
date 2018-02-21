# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception, content_disposition


class Binary(http.Controller):

    @http.route('/web/binary/download_document/<model("tax.report"):tax>', type='http', auth="user")
    @serialize_exception
    def download_document(self, tax, **kw):
        if tax.type == 'b2b':
            res = tax.print_b2b_report_excel_data()
            filename = len(res) == 2 and res[1] or 'B2B Tax Report'
        elif tax.type == 'b2c':
            res = tax.b2c_excel_report()
            filename = 'B2c Tax Report'
        elif tax.type == 'gstr1':
            res = tax.print_gstr1_report_excel_data()
            filename = len(res) == 2 and res[1] or 'GSTR1 Report'
        elif tax.type == 'b2c_summary':
            res = tax.print_b2c_summary_excel_data()
            filename = len(res) == 2 and res[1] or 'B2C Summary Report'
        else:
            res = tax.print_report_excel_data()
            filename = len(res) == 2 and res[1] or 'Tax Report'

        data = res and res[0] or ''
        filecontent = base64.b64decode(data)
        if not filecontent:
            return request.not_found()
        else:
            return request.make_response(filecontent,
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition', content_disposition(filename + '.xls'))])
