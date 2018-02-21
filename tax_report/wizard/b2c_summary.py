# -*- coding: utf-8 -*-
import datetime
import base64
import xlwt
from xlwt import easyxf
from odoo import api, models

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


class TaxReport(models.TransientModel):

    _inherit = "tax.report"

    @api.multi
    def print_b2c_summary_excel_data(self):
        sheet_name = 'B2C Summary Report'
        heading_style = xlwt.easyxf('font: bold on, height 250;')
        address_format_style = xlwt.easyxf('font: height 200;')
        phone_format = easyxf(
            'font: height 200;'
            'borders: bottom thin;'
        )
        after_heading_style = xlwt.easyxf('font: bold on, height 250;')
        voucher_of_style = xlwt.easyxf('font: bold on, height 200;')
        center_date_style = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
        )
        table_details_right_side_style = easyxf(
            'align: horizontal right;'
            'font: height 200;'
        )
        table_first_line_center_style = easyxf(
            'align: horizontal center;'
            'font: bold on, height 200;'
            'borders: top thin;'
        )
        table_first_line_right_style = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: top thin;'

        )
        table_second_line_border_style = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: bottom thin;'
        )
        grand_total_second_line = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: top thin, bottom thin;'
        )

        wb = xlwt.Workbook(encoding="UTF-8")
        ws = wb.add_sheet('GSTR1 Table7 VchDrilldown')

        address1 = ''
        address2 = ''
        if self.env.user.company_id.street:
            address1 += self.env.user.company_id.street
        if self.env.user.company_id.street2:
            address2 += self.env.user.company_id.street2

        # Company Address Part START
        ws.row(0).height = 350
        ws.write_merge(0, 0, 0, 2, self.env.user.company_id.name, heading_style)
        ws.write_merge(1, 1, 0, 2, address1, address_format_style)
        ws.write_merge(2, 2, 0, 2, address2, address_format_style)
        ws.write_merge(3, 3, 0, 2, 'CC: ' + self.env.user.company_id.phone, phone_format)
        # Company Address Part END

        # After Company Part START
        ws.row(4).height = 350
        ws.write_merge(4, 4, 0, 2, 'Voucher Register', after_heading_style)
        # After Company Part END

        # Date Part START
        if self.date_from and self.date_to:
            ws.write_merge(5, 5, 0, 2, datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y'), address_format_style)
        # Date Part END

        # After date part START
        date_content = datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y')
        ws.write_merge(6, 6, 0, 0, 'Vouchers of :', address_format_style)
        ws.write_merge(6, 6, 1, 1, 'B2C(Small) Invoices', voucher_of_style)
        ws.write_merge(6, 6, 2, 6, date_content, center_date_style)
        # After date part END

        # State Name Part START
        # Fetch all Invoices which are date between
        b2c_invoices = self.env['account.invoice'].search([('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to), ('date_invoice', '!=', False), ('partner_id.gst_number', '=', False), ('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'paid')], order="date_invoice")

        # Fetch invoice related state
        state_ids = b2c_invoices.mapped('partner_id.state_id')

        table_first_line_list = ['Particulars', 'Taxable', 'Integrated Tax', 'Central Tax', 'State Tax', 'Cess', 'Total Tax']
        table_second_line_list = ['', 'Value', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount']

        # customer_name_width = invoice_name = []

        state_name = 7
        for col, table_heading in enumerate(table_first_line_list):
            if col == 0:
                ws.write(state_name, col, table_heading, table_first_line_center_style)
            else:
                ws.write(state_name, col, table_heading, table_first_line_right_style)

        state_name += 1
        for col, table_heading in enumerate(table_second_line_list):
            ws.write(state_name, col, table_heading, table_second_line_border_style)

        state_name += 1
        total_taxable_amount = total_igst_amount_amount = total_tax_amount = 0
        state_column_width = []
        for state in state_ids:
            state_column_width.append(len(state.name))
            state_invoices = b2c_invoices.filtered(lambda i: i.partner_id.state_id.id == state.id)
            taxable = igst = cgst = sgst = cess = total_amount = 0
            for inv in state_invoices:
                taxable += inv.amount_untaxed
                igst += inv.total_igst_amount
                cgst += inv.total_cgst_amount
                sgst += inv.total_sgst_amount
                total_amount += inv.amount_total
            total_taxable_amount += taxable
            total_igst_amount_amount += igst
            total_tax_amount += total_amount
            ws.write(state_name, 0, state.name or '', table_details_right_side_style)
            ws.write(state_name, 1, taxable or '', table_details_right_side_style)
            ws.write(state_name, 2, igst or '', table_details_right_side_style)
            ws.write(state_name, 3, cgst or '', table_details_right_side_style)
            ws.write(state_name, 4, sgst or '', table_details_right_side_style)
            ws.write(state_name, 5, cess or '', table_details_right_side_style)
            ws.write(state_name, 6, total_amount or '', table_details_right_side_style)

            state_name += 1

        for cell in range(0, 7):
            if cell == 1:
                ws.write(state_name, 1, total_taxable_amount or '', grand_total_second_line)
            elif cell == 2:
                ws.write(state_name, 2, total_igst_amount_amount or '', grand_total_second_line)
            elif cell == 6:
                ws.write(state_name, 6, total_tax_amount or '', grand_total_second_line)
            else:
                ws.write(state_name, cell, '', grand_total_second_line)

        # # SET Column Width START
        ws.col(0).width = (max(state_column_width) * 3) * 100
        ws.col(1).width = 6000
        for length in range(2, 8):
            ws.col(length).width = 4000
        # # SET Column Width END

        fp = StringIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return (base64.b64encode(data), sheet_name)

    @api.multi
    def print_b2c_summary_report_excel(self):
        self.ensure_one()
        self.type = 'b2c_summary'
        return {'type': 'ir.actions.act_url',
                'name': "test",
                'url': '/web/binary/download_document/%s' % self.id,
                }
