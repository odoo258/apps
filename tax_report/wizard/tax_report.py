# -*- coding: utf-8 -*-
import datetime
import base64
import xlwt
from odoo import api, fields, models

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


class AccountInvoice(models.Model):

    _inherit = "account.invoice"
    _order = "date_invoice asc"


class TaxReport(models.TransientModel):
    _name = "tax.report"
    _description = "Tax Report"

    date_from = fields.Date()
    date_to = fields.Date()
    target_moves = fields.Selection([('all_entries', 'All Entries'), ('all_posted', 'All Posted Entries')], 'Target Moves', default='all_entries')
    report_for = fields.Selection([('all', 'All Taxes'), ('manual', 'Manual Selection')], 'Tax Report', default='all')
    display_detail = fields.Boolean('Display Detail')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    type = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C'), ('gstr1', 'GSTR1'), ('b2c_summary', 'B2C Summary')], string="Type")

    @api.multi
    def _print_report(self, data):
        return self.env['report'].get_action(self, 'tax_report.report_tax_report', data=data)

    @api.multi
    def _compute_paid_lines(self):
        tax_id = False
        lines_final = []
        move_lines = False
        if self.target_moves == 'all_entries':
            if self.report_for == 'all':
                move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', '!=', False)], order='date asc')
            else:
                move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', 'in', self.tax_ids.ids)], order='date asc')
        else:
            move_lines_posted = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', '!=', False)], order='date asc').filtered(lambda l: l.move_id.state == 'posted')
            if move_lines:
                if self.report_for == 'all':
                    move_lines = move_lines_posted
                else:
                    move_lines = move_lines_posted.filtered(lambda l: l.tax_line_id in self.tax_ids.ids)
        taxes = self.env['account.tax'].search([('type_tax_use', '=', 'purchase')])
        grand_total_tax = 0.0
        grand_total_base = 0.0
        for tax in taxes:
            tax_id = tax.id
            total_tax = 0.0
            total_base = 0.0
            sublines = []
            for line in move_lines.filtered(lambda l: l.tax_line_id == tax):
                vals = {
                    'name': line.move_id.name,
                    'tax_amt': line.debit - line.credit,
                    'partner_name': line.partner_id.name,
                    'accounting_date': line.date,
                    'ref': line.move_id.ref,
                    'gstin': line.partner_id.gst_number,
                }
                invoice = self.env['account.invoice'].search([('move_id', '=', line.move_id.id)])
                if invoice:
                    total_base_line = 0.0
                    for inv_line in invoice.invoice_line_ids.filtered(lambda t: tax_id in t.invoice_line_tax_ids.ids):
                        if invoice.type in['in_invoice', 'out_refund']:
                            total_base_line += inv_line.amount
                            total_base += inv_line.amount
                            vals.update({'base_amt': total_base_line})
                        else:
                            total_base_line -= inv_line.amount
                            total_base -= inv_line.amount
                            vals.update({'base_amt': total_base_line})
                sublines.append(vals)
                total_tax += line.debit - line.credit
            grand_total_base += total_base
            grand_total_tax += total_tax
            lines_final.append(
                {
                    'name': tax.name,
                    'base_amt': total_base,
                    'tax_amt': total_tax,
                    'partner_name': False,
                    'accounting_date': False,
                    'ref': False,
                    'gstin': False,
                    'level': 0
                })
            for sub in sublines:
                lines_final.append(
                    {
                        'name': sub.get('name'),
                        'base_amt': sub.get('base_amt'),
                        'tax_amt': sub.get('tax_amt'),
                        'partner_name': sub.get('partner_name'),
                        'accounting_date': datetime.datetime.strptime(sub.get('accounting_date'), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        'ref': sub.get('ref'),
                        'gstin': sub.get('gstin'),
                        'level': 1
                    })
        lines_final.extend([grand_total_base, grand_total_tax])
        return lines_final

    @api.multi
    def _compute_received_lines(self):
        tax_id = False
        lines_final = []
        move_lines = False
        if self.target_moves == 'all_entries':
            if self.report_for == 'all':
                move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', '!=', False)], order='date asc')
            else:
                move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', 'in', self.tax_ids.ids)], order='date asc')
        else:
            move_lines_posted = []
            account_move_line = self.env['account.move.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('tax_line_id', '!=', False)], order='date asc')
            if account_move_line:
                move_lines_posted = account_move_line.filtered(lambda l: l.move_id.state == 'posted')
            if move_lines:
                if self.report_for == 'all':
                    move_lines = move_lines_posted
                else:
                    move_lines = move_lines_posted.filtered(lambda l: l.tax_line_id in self.tax_ids.ids)
        taxes = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        grand_total_tax = 0.0
        grand_total_base = 0.0
        for tax in taxes:
            tax_id = tax.id
            total_tax = 0.0
            total_base = 0.0
            sublines = []
            for line in move_lines.filtered(lambda l: l.tax_line_id == tax):
                vals = {
                    'name': line.move_id.name,
                    'tax_amt': line.debit - line.credit,
                    'partner_name': line.partner_id.name,
                    'accounting_date': line.date,
                    'ref': line.move_id.ref,
                    'gstin': line.partner_id.gst_number
                }
                invoice = self.env['account.invoice'].search([('move_id', '=', line.move_id.id)])
                if invoice:
                    total_base_line = 0.0
                    for inv_line in invoice.invoice_line_ids.filtered(lambda t: tax_id in t.invoice_line_tax_ids.ids):
                        if invoice.type in['in_invoice', 'out_refund']:
                            total_base_line += inv_line.amount
                            total_base += inv_line.amount
                            vals.update({'base_amt': total_base_line})
                        else:
                            total_base_line -= inv_line.amount
                            total_base -= inv_line.amount
                            vals.update({'base_amt': total_base_line})

                sublines.append(vals)
                total_tax += line.debit - line.credit
            grand_total_base += total_base
            grand_total_tax += total_tax
            lines_final.append(
                {
                    'name': tax.name,
                    'base_amt': total_base,
                    'tax_amt': total_tax,
                    'partner_name': False,
                    'accounting_date': False,
                    'ref': False,
                    'gstin': False,
                    'level': 0
                })
            for sub in sublines:
                lines_final.append(
                    {
                        'name': sub.get('name'),
                        'base_amt': sub.get('base_amt'),
                        'tax_amt': sub.get('tax_amt'),
                        'partner_name': sub.get('partner_name'),
                        'accounting_date': datetime.datetime.strptime(sub.get('accounting_date'), '%Y-%m-%d').strftime('%d-%m-%Y'),
                        'ref': sub.get('ref'),
                        'gstin': sub.get('gstin'),
                        'level': 1
                    })
        lines_final.extend([grand_total_base, grand_total_tax])
        return lines_final

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to'])[0]
        data['form']['target_moves'] = self.target_moves
        data['form']['report_for'] = self.report_for
        data['form']['display_detail'] = self.display_detail
        paid_lines = self._compute_paid_lines()
        received_lines = self._compute_received_lines()
        data['paid_lines'] = paid_lines[:-2]
        data['received_lines'] = received_lines[:-2]
        data['paid_grand_base'] = paid_lines[-2]
        data['paid_grand_tax'] = paid_lines[-1]
        data['received_grand_base'] = received_lines[-2]
        data['received_grand_tax'] = received_lines[-1]
        return self._print_report(data)

    @api.multi
    def print_report_excel_data(self):
        self.ensure_one()

        sheet_name = 'Tax Report'
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Tax Report1')
        sheet.col(0).width = 256 * 35
        sheet.col(1).width = 256 * 20
        sheet.col(2).width = 256 * 20
        sheet.col(3).width = 256 * 40
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20

        # sheet style
        font = xlwt.Font()  # Create the Font
        style = xlwt.XFStyle()  # Create the Style
        style.font = font  # Apply the Font to the Style
        heading = xlwt.easyxf('font: bold on, height 300; align: horiz center;')
        bold = xlwt.easyxf('font: bold on')
        cell = xlwt.easyxf('font: bold on, height 200; align: horiz center;')
        total = xlwt.easyxf('font: bold on, height 220; align: horiz right;')
        center = xlwt.easyxf('align: horiz center;')
        # Main Info
        # sheet.write(0, 0, "Tax Report", heading)
        sheet.write_merge(0, 1, 0, 6, "Tax Report", heading)
        sheet.write(2, 0, "Date From:", total)
        sheet.write(3, 0, "Date To:", total)
        sheet.write(2, 1, datetime.datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%d-%m-%Y'))
        sheet.write(3, 1, datetime.datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%d-%m-%Y'))

        # Header
        sheet.write(5, 0, "Name", cell)
        sheet.write(5, 1, "Base Amount", cell)
        sheet.write(5, 2, "Tax Amount", cell)
        sheet.write(5, 3, "Partner", cell)
        sheet.write(5, 4, "Accounting Date", cell)
        sheet.write(5, 5, "Ref", cell)
        sheet.write(5, 6, "GSTIN", cell)
        sheet.write(6, 0, "Taxes Paid", bold)
        count_paid = 7
        lines = self._compute_paid_lines()
        sheet.write(6, 2, lines[-1], total)

        for line in lines[:-2]:
            if line.get('level') == 0:
                sheet.write(count_paid, 0, line.get('name') or '', bold)
                sheet.write(count_paid, 1, line.get('base_amt') or '', bold)
                sheet.write(count_paid, 2, line.get('tax_amt') or '', bold)
                sheet.write(count_paid, 3, line.get('partner_name') or '', bold)
                sheet.write(count_paid, 4, line.get('accounting_date') or '', bold)
                sheet.write(count_paid, 5, line.get('ref') or '', bold)
                sheet.write(count_paid, 6, line.get('gstin') or '', bold)
            else:
                sheet.write(count_paid, 0, '    ' + str(line.get('name') or ''))
                sheet.write(count_paid, 1, line.get('base_amt') or '')
                sheet.write(count_paid, 2, line.get('tax_amt') or '')
                sheet.write(count_paid, 3, line.get('partner_name') or '')
                sheet.write(count_paid, 4, line.get('accounting_date') or '', center)
                sheet.write(count_paid, 5, line.get('ref') or '', center)
                sheet.write(count_paid, 6, line.get('gstin') or '', center)
            count_paid += 1

        count_received = count_paid + 2
        received_lines = self._compute_received_lines()
        sheet.write(count_paid + 1, 0, "Taxes Received", bold)
        sheet.write(count_paid + 1, 2, received_lines[-1], total)

        for line in received_lines[:-2]:
            if line.get('level') == 0:
                sheet.write(count_received, 0, line.get('name') or '', bold)
                sheet.write(count_received, 1, line.get('base_amt') or '', bold)
                sheet.write(count_received, 2, line.get('tax_amt') or '', bold)
                sheet.write(count_received, 3, line.get('partner_name') or '', bold)
                sheet.write(count_received, 4, line.get('accounting_date') or '', bold)
                sheet.write(count_received, 5, line.get('ref') or '', bold)
                sheet.write(count_received, 6, line.get('gstin') or '', bold)
            else:
                sheet.write(count_received, 0, '    ' + str(line.get('name') or ''))
                sheet.write(count_received, 1, line.get('base_amt') or '')
                sheet.write(count_received, 2, line.get('tax_amt') or '')
                sheet.write(count_received, 3, line.get('partner_name') or '')
                sheet.write(count_received, 4, line.get('accounting_date') or '', center)
                sheet.write(count_received, 5, line.get('ref') or '', center)
                sheet.write(count_received, 6, line.get('gstin') or '', center)
            count_received += 1

        # Total
        sheet.write(count_received, 1, lines[-2] + received_lines[-2], total)
        sheet.write(count_received, 2, lines[-1] + received_lines[-1], total)

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return (base64.b64encode(data), sheet_name)

    @api.multi
    def print_report_excel(self):
        self.ensure_one()
        self.type = False
        return {'type': 'ir.actions.act_url',
                'name': "test",
                'url': '/web/binary/download_document/%s' % self.id
                }
