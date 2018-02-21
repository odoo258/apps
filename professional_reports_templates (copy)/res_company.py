# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Account_config(models.TransientModel):
    _name = "account.report.default_settings"

    report_logo = fields.Binary(string="Report Logo")

    account_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Default Invoice Template')
    template_base_color = fields.Char(string="Template Base Color",
    help="Choose your color")
    template_text_color = fields.Char(string="Template Text Color",
    help="Choose your color")
    general_text_color = fields.Char(string="General Text Color",
    help="Choose your color")
    company_name_color = fields.Char(string="Company Name Color",
    help="Choose your color")
    company_adddress_color = fields.Char(string="Company Address Color",
    help="Choose your color")
    is_comany_name_bold = fields.Boolean(string="Display company name in Bold")

    report_watermark_logo = fields.Binary(string="Report Watermark Logo")
    table_odd_parity_color = fields.Char(string="Table Odd Parity Color",
    help="Choose your color")
    table_even_parity_color = fields.Char(string="Table Even Parity Color",
    help="Choose your color")
    customer_name_color= fields.Char(string="Customer Name Color",
    help="Choose your color")
    customer_address_color= fields.Char(string="Customer Address Color",
    help="Choose your color")
    display_product_description = fields.Boolean(string="Display Product Description")
    display_customer_name_bold = fields.Boolean(string="Display Customer Name in Bold")


class ResPrtnerInherited(models.Model):
    _inherit = "res.partner"

    account_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Default Invoice Template')
    



class account_invoice(models.Model):
    _inherit = "account.invoice"

    account_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Default Invoice Template')


    @api.multi
    def invoice_print(self):
    #     """ Print the invoice and mark it as sent, so that we can see more
    #         easily the next step of the workflow
    #     """

        settings_object = self.env['account.report.default_settings'].search([])

        
    #     import pdb
    #     pdb.set_trace()
    #     self.ensure_one()
    #     # self.sent = True
    #     return self.env['report'].get_action(self.settings_object, 'bi_professional_reports_templates.report_invoice')

