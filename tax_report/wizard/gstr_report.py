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


class AccountInvoice(models.Model):

    _inherit = "account.invoice"
    _order = "date_invoice asc"


class TaxReport(models.TransientModel):

    _inherit = "tax.report"

    @api.multi
    def print_gstr1_report_excel_data(self):
        self.ensure_one()

        sheet_name = 'GSTR1 Report'
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('GSTR1')
        sheet.col(0).width = 256 * 12
        sheet.col(1).width = 256 * 20
        sheet.col(2).width = 256 * 12
        sheet.col(3).width = 256 * 15
        sheet.col(4).width = 256 * 22
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 16
        sheet.col(7).width = 256 * 8
        sheet.col(8).width = 256 * 16
        sheet.col(9).width = 256 * 16

        font = xlwt.Font()
        style = xlwt.XFStyle()
        style.font = font
        bold = xlwt.easyxf('font: bold on')
        cell = xlwt.easyxf('font: bold on, height 200; align: horizontal center;')
        heading_style = xlwt.easyxf('font: bold on, height 250;align: horizontal center;')
        address_format_style = xlwt.easyxf('font: height 200;align: horizontal center;')

        after_heading_style = xlwt.easyxf('font: bold on, height 250;'
                                          'align: horizontal center;')
        phone_format = easyxf('font: height 200;'
                              'borders: bottom thin;'
                              'align: horizontal center;'
                              )
        center_date_style = easyxf(
            'align: horizontal right;'
            'font: bold on, height 200;'
        )
        name_left_style = easyxf(
            'align: horizontal left;'
            'font: bold on, height 200;'
        )

        address1 = ''
        address2 = ''
        if self.env.user.company_id.street:
            address1 += self.env.user.company_id.street
        if self.env.user.company_id.street2:
            address2 += self.env.user.company_id.street2

        # Company Address Part START
        sheet.row(0).height = 350
        sheet.write_merge(0, 0, 0, 9, self.env.user.company_id.name, heading_style)
        sheet.write_merge(1, 1, 0, 9, address1, address_format_style)
        sheet.write_merge(2, 2, 0, 9, address2, address_format_style)
        sheet.write_merge(3, 3, 0, 9, 'CC: ' + self.env.user.company_id.phone, phone_format)
        # Company Address Part END

        # After Company Part START
        sheet.row(4).height = 350
        sheet.write_merge(4, 4, 0, 9, 'GST Computation', after_heading_style)
        # After Company Part END

        # Date Part START
        if self.date_from and self.date_to:
            sheet.write_merge(5, 5, 0, 9, datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y'), address_format_style)
        # Date Part END

        # After date part START
        date_content = datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%b-%Y') + ' to ' + datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%b-%Y')
        sheet.write_merge(6, 6, 0, 4, 'GSTR-1', name_left_style)
        sheet.write_merge(6, 6, 5, 9, date_content, center_date_style)
        # After date part END

        sheet.write_merge(7, 7, 0, 4, 'Returns Summary', name_left_style)
        sheet.write_merge(7, 7, 5, 9, '', center_date_style)
        sheet.write_merge(8, 8, 0, 4, 'Total number of vouchers for the period', name_left_style)
        sheet.write_merge(8, 8, 5, 9, '', center_date_style)
        sheet.write_merge(9, 9, 0, 4, 'Included in returns', address_format_style)
        sheet.write_merge(9, 9, 5, 9, '', center_date_style)
        sheet.write_merge(10, 10, 0, 4, 'Not relevant for returns', address_format_style)
        sheet.write_merge(10, 10, 5, 9, '', center_date_style)
        sheet.write_merge(11, 11, 0, 4, 'Incomplete/Mismatch in information (to be resolved)', address_format_style)
        sheet.write_merge(11, 11, 5, 9, '', center_date_style)

        sheet.write(12, 0, "Table No.", cell)
        sheet.write(12, 1, "Particulars", cell)
        sheet.write(12, 2, "Count", cell)
        sheet.write(12, 3, "Taxable Value", cell)
        sheet.write(12, 4, "Integrated Tax Amount", cell)
        sheet.write(12, 5, "Central Tax Amount", cell)
        sheet.write(12, 6, "State Tax Amount", bold)
        sheet.write(12, 7, "Cess Amount", bold)
        sheet.write(12, 8, "Tax Amount", bold)
        sheet.write(12, 9, "Invoice Amount", bold)

        row = 14
        b2b_invoices = self.env['account.invoice'].search([('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to), ('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'paid')], order="date_invoice")
        total_taxable_amount_b2b = total_taxable_b2b_igst = total_taxable_b2b_cgst = total_taxable_b2b_sgst = total_taxable_b2b_gst_tax = b2b_amount_total = 0
        for b2b_invoice in b2b_invoices:
            sale_order = self.env['sale.order'].search([('name', '=', str(b2b_invoice.origin))])
            if sale_order and sale_order.partner_id.gst_number:
                total_taxable_amount_b2b += b2b_invoice.amount_untaxed
                total_taxable_b2b_igst += b2b_invoice.total_igst_amount
                total_taxable_b2b_cgst += b2b_invoice.total_cgst_amount
                total_taxable_b2b_sgst += b2b_invoice.total_sgst_amount
                total_taxable_b2b_gst_tax += b2b_invoice.total_gst_tax_amount
                b2b_amount_total += b2b_invoice.amount_total

        b2c_invoices = self.env['account.invoice'].search([('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to), ('date_invoice', '!=', False), ('partner_id.parent_id.gst_number', '=', False), ('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'paid')], order="date_invoice")
        total_taxable_amount_b2c = total_taxable_b2c_igst = total_taxable_b2c_cgst = total_taxable_b2c_sgst = total_taxable_b2c_gst_tax = b2c_amount_total = 0
        for b2c_invoice in b2c_invoices:
            total_taxable_amount_b2c += b2c_invoice.amount_untaxed
            total_taxable_b2c_igst += b2c_invoice.total_igst_amount
            total_taxable_b2c_cgst += b2c_invoice.total_cgst_amount
            total_taxable_b2c_sgst += b2c_invoice.total_sgst_amount
            total_taxable_b2c_gst_tax += b2c_invoice.total_gst_tax_amount
            b2c_amount_total += b2c_invoice.amount_total

        sheet.write(row, 0, '5' or '')
        sheet.write(row, 1, 'B2B Invoices' or '')
        sheet.write(row, 2, len(b2b_invoices) or '')
        sheet.write(row, 3, total_taxable_amount_b2b or '')
        sheet.write(row, 4, total_taxable_b2b_igst or '')
        sheet.write(row, 5, total_taxable_b2b_cgst or '')
        sheet.write(row, 6, total_taxable_b2b_sgst or '')
        sheet.write(row, 7, '', bold)
        sheet.write(row, 8, total_taxable_b2b_gst_tax or '')
        sheet.write(row, 9, b2b_amount_total or '')

        row += 1

        sheet.write(row, 0, '6' or '')
        sheet.write(row, 1, 'B2C(Small) Invoices' or '')
        sheet.write(row, 2, len(b2c_invoices) or '')
        sheet.write(row, 3, total_taxable_amount_b2c or '')
        sheet.write(row, 4, total_taxable_b2c_igst or '')
        sheet.write(row, 5, total_taxable_b2c_cgst or '')
        sheet.write(row, 6, total_taxable_b2c_sgst or '')
        sheet.write(row, 7, '', bold)
        sheet.write(row, 8, total_taxable_b2c_gst_tax or '')
        sheet.write(row, 9, b2c_amount_total or '')

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return (base64.b64encode(data), sheet_name)

    @api.multi
    def print_gstr1_report_excel(self):
        self.ensure_one()
        self.type = 'gstr1'
        return {'type': 'ir.actions.act_url',
                'name': "test",
                'url': '/web/binary/download_document/%s' % self.id,
                }
