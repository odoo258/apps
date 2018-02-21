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

    def print_b2c_excel_data(self, ws, inv_id, customer_name_width, invoice_name, state_name, table_details_right_side_style, table_details_left_side_style):
        customer_name_width.append(len(inv_id.partner_id.name))
        invoice_name.append(len(inv_id.display_name))
        ws.write(state_name, 0, inv_id.date_invoice or '', table_details_right_side_style)
        sale_order = False
        if inv_id.origin:
            sale_order = self.env['sale.order'].search([('name', '=', str(inv_id.origin))])
        ws.write(state_name, 1, sale_order.partner_id.name if sale_order else inv_id.partner_id.name or '', table_details_left_side_style)
        ws.write(state_name, 2, '', table_details_right_side_style)
        ws.write(state_name, 3, 'Sales' if inv_id.type == 'out_invoice' else 'Credit Note', table_details_left_side_style)
        ws.write(state_name, 4, inv_id.display_name or '', table_details_right_side_style)
        ws.write(state_name, 5, inv_id.amount_untaxed or '', table_details_right_side_style)
        ws.write(state_name, 6, inv_id.total_igst_amount or '', table_details_right_side_style)
        ws.write(state_name, 7, inv_id.total_cgst_amount or '', table_details_right_side_style)
        ws.write(state_name, 8, inv_id.total_sgst_amount or '', table_details_right_side_style)
        ws.write(state_name, 9, '', table_details_right_side_style)
        ws.write(state_name, 10, inv_id.total_gst_tax_amount or '', table_details_right_side_style)
        ws.write(state_name, 11, inv_id.amount_total or '', table_details_right_side_style)

    def grand_total_line_part(self, ws, state_name, grand_total_first_line, grand_total_second_line, taxable_value, igst, total_tax, total_invoice):
        for cell in range(0, 12):
            if cell == 1:
                ws.write(state_name, 1, 'Grand Total', grand_total_first_line)
            elif cell == 5:
                ws.write(state_name, 5, taxable_value or '', grand_total_second_line)
            elif cell == 6:
                ws.write(state_name, 6, igst or '', grand_total_second_line)
            elif cell == 10:
                ws.write(state_name, 10, total_tax or '', grand_total_second_line)
            elif cell == 11:
                ws.write(state_name, 11, total_invoice or '', grand_total_second_line)
            elif cell != 1 or cell != 5 or cell != 6 or cell != 10 or cell != 11:
                ws.write(state_name, cell, '', grand_total_second_line)

    @api.multi
    def b2c_excel_report(self):
        sheet_name = 'B2C Tax Report'
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
        table_details_left_side_style = easyxf(
            'align: horizontal left;'
            'font: height 200;'
        )
        table_details_right_side_style = easyxf(
            'align: horizontal right;'
            'font: height 200;'
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
        ws.write_merge(4, 4, 0, 2, 'GSTR1 Table7 VchDrilldown', after_heading_style)
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
        b2c_invoices = self.env['account.invoice'].search([('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to), ('date_invoice', '!=', False), ('partner_id.parent_id.gst_number', '=', False), ('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'paid')], order="date_invoice")
        # Fetch invoice related state
        state_ids = b2c_invoices.mapped('partner_id.state_id')

        state_name = 7
        table_first_line_list = ['Date', 'Particulars', 'GSTIN/UIN', 'Vch Type', 'Vch No.', 'Taxable', 'Integrated Tax', 'Central Tax', 'State Tax', 'Cess', 'Total Tax', 'Invoice']
        table_second_line_list = ['', '', '', '', '', 'Value', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount']

        customer_name_width = invoice_name = []

        for state in state_ids:
            # For state Heading
            ws.write(state_name, 0, 'For State :', address_format_style)
            ws.write(state_name, 1, state.name, voucher_of_style)
            # For state Heading

            state_name += 1
            state_invoices = b2c_invoices.filtered(lambda i: i.partner_id.state_id.id == state.id)
            for col, table_heading in enumerate(table_first_line_list):
                if col == 1 or col == 2 or col == 3:
                    ws.write(state_name, col, table_heading, table_first_line_border_style)
                else:
                    ws.write(state_name, col, table_heading, table_first_line_border_top)
            state_name += 1
            for col, table_heading in enumerate(table_second_line_list):
                ws.write(state_name, col, table_heading, table_second_line_border_style)

            invoices = state_invoices.filtered(lambda i: i.type == 'out_invoice')
            refund_invoices = state_invoices.filtered(lambda r: r.type == 'out_refund')

            state_name += 1

            if invoices:
                sale_total_taxable_value = sale_integrated_tax_amount = sale_total_tax_amount = sale_total_invoice_amount = 0
                for cell, inv_id in enumerate(invoices):

                    sale_total_taxable_value += inv_id.amount_untaxed
                    sale_integrated_tax_amount += inv_id.total_igst_amount
                    sale_total_tax_amount += inv_id.total_gst_tax_amount
                    sale_total_invoice_amount += inv_id.amount_total
                    self.print_b2c_excel_data(ws, inv_id, customer_name_width, invoice_name, state_name, table_details_right_side_style, table_details_left_side_style)
                    state_name += 1

                # Grand Total Part START
                self.grand_total_line_part(ws, state_name, grand_total_first_line, grand_total_second_line, sale_total_taxable_value, sale_integrated_tax_amount, sale_total_tax_amount, sale_total_invoice_amount)
                # Grand Total Part END

            state_name += 1

            if refund_invoices:
                credit_note_total_taxable_value = credit_note_integrated_tax_amount = credit_note_total_tax_amount = credit_note_total_invoice_amount = 0
                for cell, inv_id in enumerate(refund_invoices):

                    credit_note_total_taxable_value += inv_id.amount_untaxed
                    credit_note_integrated_tax_amount += inv_id.total_igst_amount
                    credit_note_total_tax_amount += inv_id.total_gst_tax_amount
                    credit_note_total_invoice_amount += inv_id.amount_total
                    self.print_b2c_excel_data(ws, inv_id, customer_name_width, invoice_name, state_name, table_details_right_side_style, table_details_left_side_style)
                    state_name += 1

                # Grand Total Part START
                self.grand_total_line_part(ws, state_name, grand_total_first_line, grand_total_second_line, credit_note_total_taxable_value, credit_note_integrated_tax_amount, credit_note_total_tax_amount, credit_note_total_invoice_amount)
                # Grand Total Part END

            state_name += 6
            # State Name Part END

        # SET Column Width START
        ws.col(0).width = 3200
        ws.col(1).width = ((max(customer_name_width) + 8) * 2) * 100
        ws.col(4).width = ((max(invoice_name) + 2) * 2) * 100
        ws.col(6).width = 5000
        ws.col(7).width = 5000
        # SET Column Width END

        fp = StringIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return (base64.b64encode(data), sheet_name)

    @api.multi
    def print_b2c_excel_report(self):
        self.ensure_one()
        self.type = 'b2c'
        return {'type': 'ir.actions.act_url',
                'name': "test",
                'url': '/web/binary/download_document/%s' % self.id,
                }
