# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Account_config(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary(string="Report Logo")
    account_template = fields.Selection([
            ('advanced', 'Advanced'),
            ('creative', 'Creative'),
            ('elegant', 'Elegant'),
            ('exclusive', 'Exclusive'),
            ('contemprory', 'Contemprory'),
            ('professional', 'Professional'),
        ],string='Default Invoice Template')
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

    report_watermark_logo = fields.Binary('Report Watermark Logo')
    # report_watermark_logo = fields.Binary(string="Report Watermark Logo")
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
    is_custom_footer = fields.Boolean(string="Custom Footer")
    report_footer = fields.Text(string="Report Footer")
    

class ResPrtnerInherited(models.Model):
    _inherit = "res.partner"

    account_template = fields.Selection(related='company_id.account_template', string="Invoice Template")


class account_invoice(models.Model):
    _inherit = "account.invoice"

    account_template = fields.Selection(related='company_id.account_template', string="Invoice Template")


class IrActionsReportXmlPdf(models.Model):
    _inherit = 'ir.actions.report.xml'

    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.user.company_id, help="Company related to this journal")
    pdf_watermark = fields.Binary(related='company_id.report_watermark_logo')
    