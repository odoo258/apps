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

    def print_b2b_report_data(self, sheet, row, b2b_invoice, bold):
        sheet.write(row, 0, b2b_invoice.date_invoice or '')

        sheet.write(row, 1, b2b_invoice.partner_id.parent_id.name if b2b_invoice.partner_id.parent_id.name else b2b_invoice.partner_id.name or '')
        sheet.write(row, 2, b2b_invoice.partner_id.parent_id.gst_number if b2b_invoice.partner_id.parent_id.gst_number else b2b_invoice.partner_id.gst_number)
        sheet.write(row, 3, 'Sales' if b2b_invoice.type == 'out_invoice' else 'Credit Note')
        sheet.write(row, 4, b2b_invoice.display_name or '')
        sheet.write(row, 5, b2b_invoice.amount_untaxed or '')
        sheet.write(row, 6, b2b_invoice.total_igst_amount or '')
        sheet.write(row, 7, b2b_invoice.total_cgst_amount or '')
        sheet.write(row, 8, b2b_invoice.total_sgst_amount or '')
        sheet.write(row, 9, '', bold)
        sheet.write(row, 10, b2b_invoice.total_gst_tax_amount or '')
        sheet.write(row, 11, b2b_invoice.amount_total or '')

    def grand_total_invoice_line(self, sheet, row, grand_total_first_line, grand_total_second_line, taxable, igst, cgst, sgst, total_tax, total_invoice):
        for cell in range(0, 12):
            if cell == 0 or cell == 2 or cell == 3 or cell == 4 or cell == 9:
                sheet.write(row, cell, '', grand_total_second_line)
            elif cell == 1:
                sheet.write(row, cell, 'Grand Total', grand_total_first_line)
            elif cell == 5:
                sheet.write(row, cell, taxable, grand_total_second_line)
            elif cell == 6:
                sheet.write(row, cell, igst, grand_total_second_line)
            elif cell == 7:
                sheet.write(row, cell, cgst, grand_total_second_line)
            elif cell == 8:
                sheet.write(row, cell, sgst, grand_total_second_line)
            elif cell == 10:
                sheet.write(row, cell, total_tax, grand_total_second_line)
            elif cell == 11:
                sheet.write(row, cell, total_invoice, grand_total_second_line)

    @api.multi
    def print_b2b_report_excel_data(self):
        self.ensure_one()

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
        table_first_line_border_style = easyxf(
            'align: horizontal left;'
            'font: bold on, height 200;'
            'borders: top thin;'
        )
        table_first_line_border_top = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: top thin;'
        )
        table_second_line_border_style = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: bottom thin;'
        )
        grand_total_first_line = easyxf(
            'align: horizontal left;'
            'font: bold on, height 200;'
            'borders: top thin, bottom thin;'
        )
        grand_total_second_line = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
            'borders: top thin, bottom thin;'
        )

        sheet_name = 'B2B Tax Report'
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Tax Report1')
        sheet.col(0).width = 256 * 12
        sheet.col(1).width = 256 * 26
        sheet.col(2).width = 256 * 20
        sheet.col(3).width = 256 * 12
        sheet.col(4).width = 256 * 24
        sheet.col(5).width = 256 * 12
        sheet.col(6).width = 5000
        sheet.col(7).width = 256 * 12
        sheet.col(8).width = 256 * 12
        sheet.col(9).width = 256 * 8
        sheet.col(10).width = 256 * 12
        sheet.col(11).width = 256 * 12

        # sheet style
        font = xlwt.Font()  # Create the Font
        style = xlwt.XFStyle()  # Create the Style
        style.font = font  # Apply the Font to the Style
        bold = xlwt.easyxf('font: bold on')
        # Main Info
        # sheet.write(0, 0, "Tax Report", heading)
        address1 = ''
        address2 = ''
        if self.env.user.company_id.street:
            address1 += self.env.user.company_id.street
        if self.env.user.company_id.street2:
            address2 += self.env.user.company_id.street2

        # Company Address Part START
        sheet.row(0).height = 350
        sheet.write_merge(0, 0, 0, 2, self.env.user.company_id.name, heading_style)
        sheet.write_merge(1, 1, 0, 2, address1, address_format_style)
        sheet.write_merge(2, 2, 0, 2, address2, address_format_style)
        sheet.write_merge(3, 3, 0, 2, 'CC: ' + self.env.user.company_id.phone, phone_format)
        # Company Address Part END

        # After Company Part START
        sheet.row(4).height = 350
        sheet.write_merge(4, 4, 0, 2, 'Voucher Register', after_heading_style)
        # After Company Part END

        # Date Part START
        if self.date_from and self.date_to:
            sheet.write_merge(5, 5, 0, 2, datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y'), address_format_style)
        # Date Part END

        # After date part START
        date_content = datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y')
        sheet.write_merge(6, 6, 0, 0, 'Vouchers of :', address_format_style)
        sheet.write_merge(6, 6, 1, 1, 'B2B Invoices', voucher_of_style)
        sheet.write_merge(6, 6, 2, 7, date_content, center_date_style)
        # After date part END

        state_name = 7
        table_first_line_list = ['Date', 'Particulars', 'GSTIN/UIN', 'Vch Type', 'Vch No.', 'Taxable', 'Integrated Tax', 'Central Tax', 'State Tax', 'Cess', 'Total Tax', 'Invoice']
        table_second_line_list = ['', '', '', '', '', 'Value', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount']

        for col, table_heading in enumerate(table_first_line_list):
            if col == 1 or col == 2 or col == 3:
                sheet.write(state_name, col, table_heading, table_first_line_border_style)
            else:
                sheet.write(state_name, col, table_heading, table_first_line_border_top)
        state_name += 1
        for col, table_heading in enumerate(table_second_line_list):
            sheet.write(state_name, col, table_heading, table_second_line_border_style)

        row = 9
        b2b_invoices = self.env['account.invoice'].search([('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to), ('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'paid')], order="date_invoice")

        invoices = b2b_invoices.filtered(lambda i: i.type == 'out_invoice')
        refund_invoices = b2b_invoices.filtered(lambda r: r.type == 'out_refund')

        sale_total_taxable_value = sale_integrated_tax_amount = sale_crental_tax_amount = sale_state_tax_amount = sale_total_tax_amount = sale_total_invoice_amount = 0
        credit_note_total_taxable_value = credit_note_integrated_tax_amount = credit_note_crental_tax_amount = credit_note_state_tax_amount = credit_note_total_tax_amount = credit_note_total_invoice_amount = 0

        if invoices:
            for b2b_invoice in invoices:
                sale_order = self.env['sale.order'].search([('name', '=', str(b2b_invoice.origin))])
                if sale_order and sale_order.partner_id.gst_number:
                    sale_total_taxable_value += b2b_invoice.amount_untaxed
                    sale_integrated_tax_amount += b2b_invoice.total_igst_amount
                    sale_crental_tax_amount += b2b_invoice.total_cgst_amount
                    sale_state_tax_amount += b2b_invoice.total_sgst_amount
                    sale_total_tax_amount += b2b_invoice.total_gst_tax_amount
                    sale_total_invoice_amount += b2b_invoice.amount_total
                    self.print_b2b_report_data(sheet, row, b2b_invoice, bold)
                    row += 1
            # Grand Total Part START
            if sale_total_taxable_value != 0 or sale_integrated_tax_amount != 0 or sale_crental_tax_amount != 0 or sale_state_tax_amount != 0 or sale_total_tax_amount != 0 or sale_total_invoice_amount != 0:
                self.grand_total_invoice_line(sheet, row, grand_total_first_line, grand_total_second_line, sale_total_taxable_value, sale_integrated_tax_amount, sale_crental_tax_amount, sale_state_tax_amount, sale_total_tax_amount, sale_total_invoice_amount)
            # Grand Total Part END
        row += 1
        if refund_invoices:
            for b2b_invoice in refund_invoices:
                if b2b_invoice.partner_id.parent_id.gst_number or b2b_invoice.partner_id.gst_number:
                    credit_note_total_taxable_value += b2b_invoice.amount_untaxed
                    credit_note_integrated_tax_amount += b2b_invoice.total_igst_amount
                    credit_note_crental_tax_amount += b2b_invoice.total_cgst_amount
                    credit_note_state_tax_amount += b2b_invoice.total_sgst_amount
                    credit_note_total_tax_amount += b2b_invoice.total_gst_tax_amount
                    credit_note_total_invoice_amount += b2b_invoice.amount_total
                    self.print_b2b_report_data(sheet, row, b2b_invoice, bold)
                    row += 1
            # Grand Total Part START
            if credit_note_total_taxable_value != 0 or credit_note_integrated_tax_amount != 0 or credit_note_crental_tax_amount != 0 or credit_note_state_tax_amount != 0 or credit_note_total_tax_amount != 0 or credit_note_total_invoice_amount != 0:
                self.grand_total_invoice_line(sheet, row, grand_total_first_line, grand_total_second_line, credit_note_total_taxable_value, credit_note_integrated_tax_amount, credit_note_crental_tax_amount, credit_note_state_tax_amount, credit_note_total_tax_amount, credit_note_total_invoice_amount)
            # Grand Total Part END

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return (base64.b64encode(data), sheet_name)

    @api.multi
    def print_b2b_report_excel(self):
        self.ensure_one()
        self.type = 'b2b'
        return {'type': 'ir.actions.act_url',
                'name': "test",
                'url': '/web/binary/download_document/%s' % self.id,
                }
