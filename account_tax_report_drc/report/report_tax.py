# -*- coding: utf-8 -*-

import time
from odoo import api, models


class ReportFinancial(models.AbstractModel):
    _name = 'report.account_tax_report_drc.report_tax'

    # def _compute_report_balance(self, reports, data):
    #     # print "hiii"
        

    @api.model  
    def get_account_lines(self, data):
        lines = []
        account_report = self.env['account.tax.report'].search(
            [('id', '=', data['account_tax_report_id'][0])])
        child_reports = account_report._get_children_by_order()
        # res = self.with_context(data.get('used_context')
        #                         )._compute_report_balance(child_reports, data)
        # # print res,"--------------"
        # return res
        records = {}
        lst = []
        tax_lst = []
        lines = []
        tax_name_ls = []
#         res = {}
        account_invoice = None
        if data['target_move'] == 'posted':
            account_invoice = self.env['account.invoice'].search(
                [('tax_line_ids', '!=', False), ('state', 'in', ['open', 'paid']), ('date', '>=', data['date_from']), ('date', '<=', data['date_to'])]).filtered(lambda l: l.move_id.state == 'posted')
            # print account_invoice,"------------"
        else:
            account_invoice = self.env['account.invoice'].search(
                [('tax_line_ids', '!=', False), ('state', 'in', ['open', 'paid']), ('date', '>=', data['date_from']), ('date', '<=', data['date_to'])])
        
        for report in child_reports:
        #     # check : records in account invoice having taxes incuded in account tax report.
        #     # all records of account invoice
        #     # loop for no of invoice
        #     records.update({'level': report.level})
            tax_types = self.env['account.tax.report'].search(
                [('name', '=', report.name)])

            tax_name_ls = [p.name for p in tax_types.account_tax_type_ids]
            grand_total_tax = 0.0
            grand_total_base = 0.0
            for tax in tax_name_ls:
                # tax_id = tax.id
                total_tax = 0.0
                total_base = 0.0
                sublines = []
                for line in account_invoice:
                    if line.tax_line_ids:
        #             # print rec.tax_line_ids.name
                        for tax1 in line.tax_line_ids:
                            if tax1.name in tax_name_ls:
        #                     # print tax.name
                                # print line.number
                                lines.append(line)
                print lines
        # invoice=[]
        # for li in lines:
        #     if li not in invoice:
        #         invoice.append(li.number)
        # print invoice

        # print lines            # print line
        #         vals = {
        #             'name': line.move_id.name,
        #             'tax_amt': line.debit - line.credit,
        #             'partner_name': line.partner_id.name,
        #             'accounting_date': line.date,
        #             'ref': line.move_id.ref,
        #             'gstin': line.partner_id.gst_number,
        #         }
        #         invoice = self.env['account.invoice'].search([('move_id', '=', line.move_id.id)])
        #         if invoice:
        #             total_base_line = 0.0
        #             for inv_line in invoice.invoice_line_ids.filtered(lambda t: tax_id in t.invoice_line_tax_ids.ids):
        #                 if invoice.type in['in_invoice', 'out_refund']:
        #                     total_base_line += inv_line.amount
        #                     total_base += inv_line.amount
        #                     vals.update({'base_amt': total_base_line})
        #                 else:
        #                     total_base_line -= inv_line.amount
        #                     total_base -= inv_line.amount
        #                     vals.update({'base_amt': total_base_line})
        #         sublines.append(vals)
        #         total_tax += line.debit - line.credit
        #     grand_total_base += total_base
        #     grand_total_tax += total_tax
        #     lines_final.append(
        #         {
        #             'name': tax.name,
        #             'base_amt': total_base,
        #             'tax_amt': total_tax,
        #             'partner_name': False,
        #             'accounting_date': False,
        #             'ref': False,
        #             'gstin': False,
        #             'level': 0
        #         })
        #     for sub in sublines:
        #         lines_final.append(
        #             {
        #                 'name': sub.get('name'),
        #                 'base_amt': sub.get('base_amt'),
        #                 'tax_amt': sub.get('tax_amt'),
        #                 'partner_name': sub.get('partner_name'),
        #                 'accounting_date': datetime.datetime.strptime(sub.get('accounting_date'), '%Y-%m-%d').strftime('%d-%m-%Y'),
        #                 'ref': sub.get('ref'),
        #                 'gstin': sub.get('gstin'),
        #                 'level': 1
        #             })
        # lines_final.extend([grand_total_base, grand_total_tax])
        # return lines_final
        # for report in child_reports:
        #     # check : records in account invoice having taxes incuded in account tax report.
        #     # all records of account invoice
        #     # loop for no of invoice
        #     records.update({'level': report.level})
            # tax_types = self.env['account.tax.report'].search(
            #     [('name', '=', report.name)])

            # tax_name_ls = [p.name for p in tax_types.account_tax_type_ids]
        #     # print records,"++++++++++++++"
        #     for rec in account_invoice:
        #         if rec.tax_line_ids:
        #             # print rec.tax_line_ids.name
        #             for tax in rec.tax_line_ids:
        #                 if tax.name in tax_name_ls:
        #                     # print tax.name
        #                     if tax.name not in tax_lst:
        #                         tax_lst.append(tax.name)
        #                     records = {
        #                         'bill_no': rec.number or "Name",
        #                         'tax_name': str(tax.name),
        #                         'amount': tax.amount,
        #                         'base_amount': rec.amount_untaxed,
        #                         'partner': rec.partner_id.name,
        #                         'level': report.level,
        #                     }

        #                     # lst.append(records)

        # # print records.get('level'),"kkk"
        # return records

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        # report_lines = self.get_account_lines(data.get('form'))
        report_lines = self.get_account_lines(data.get('form'))
        print report_lines
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_account_lines': report_lines,
            # 'tax_data': lst
        }
        return self.env['report'].render('account_tax_report_drc.report_tax', docargs)


# report_lines = self.get_account_lines(data.get('form'))






# # -*- coding: utf-8 -*-

# import time
# from odoo import api, models


# class ReportFinancial(models.AbstractModel):
#     _name = 'report.account_tax_report_drc.report_tax'

#     def _compute_report_balance(self, reports, data):
#         # print "hiii"
#         records = {}
#         lst = []
#         tax_lst = []
#         lines = []
# #         res = {}
#         account_invoice = None
#         if data['target_move'] == 'posted':
#             account_invoice = self.env['account.invoice'].search(
#                 [('tax_line_ids', '!=', False), ('state', 'in', ['open', 'paid']), ('date', '>=', data['date_from']), ('date', '<=', data['date_to'])]).filtered(lambda l: l.move_id.state == 'posted')
#             # print account_invoice,"------------"
#         else:
#             account_invoice = self.env['account.invoice'].search(
#                 [('tax_line_ids', '!=', False), ('state', 'in', ['open', 'paid']), ('date', '>=', data['date_from']), ('date', '<=', data['date_to'])])
        
        

#         for report in reports:
#             # check : records in account invoice having taxes incuded in account tax report.
#             # all records of account invoice
#             # loop for no of invoice
#             records = {'level': report.level}
#             tax_types = self.env['account.tax.report'].search(
#                 [('name', '=', report.name)])

#             tax_name_ls = [p.name for p in tax_types.account_tax_type_ids]
#             # print records,"++++++++++++++"
#             for rec in account_invoice:
#                 if rec.tax_line_ids:
#                     # print rec.tax_line_ids.name
#                     for tax in rec.tax_line_ids:
#                         if tax.name in tax_name_ls:
#                             # print tax.name
#                             if tax.name not in tax_lst:
#                                 tax_lst.append(tax.name)
#                             records.update({
#                                 'bill_no': rec.number or "Name",
#                                 'tax_name': str(tax.name),
#                                 'amount': tax.amount,
#                                 'base_amount': rec.amount_untaxed,
#                                 'partner': rec.partner_id.name,
#                                 # 'level': report.level,
#                             })

#                             lst.append(records)

#         # print records.get('level'),"kkk"
#         return lst

#     @api.model  
#     def get_account_lines(self, data):
#         lines = []
#         account_report = self.env['account.tax.report'].search(
#             [('id', '=', data['account_tax_report_id'][0])])
#         child_reports = account_report._get_children_by_order()
#         res = self.with_context(data.get('used_context')
#                                 )._compute_report_balance(child_reports, data)
#         # print res,"--------------"
#         return res

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_id'))

#         # report_lines = self.get_account_lines(data.get('form'))
#         report_lines = self.get_account_lines(data.get('form'))
#         print report_lines
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_account_lines': report_lines,
#             # 'tax_data': lst
#         }
#         return self.env['report'].render('account_tax_report_drc.report_tax', docargs)


# # report_lines = self.get_account_lines(data.get('form'))
