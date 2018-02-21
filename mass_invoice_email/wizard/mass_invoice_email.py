# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mass_invoice(models.TransientModel):
    _name = 'mass_invoice_mail'

    @api.one
    def send_email(self):
        """this defination send the mass mail for invoices
        """
        template_id = self.env.ref(
            'account.email_template_edi_invoice')
        active_ids = self._context['active_ids']
        for invoice_id in active_ids:
            inv_obj = self.env['account.invoice'].browse(invoice_id)
            template_id.send_mail(inv_obj.id, force_send=True)