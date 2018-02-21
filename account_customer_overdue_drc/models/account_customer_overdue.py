# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import Warning
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Wizard(models.TransientModel):
    _name = 'wizard_overdue'

    date = fields.Date(string="Date")

    def print_report(self, data):

        partners = self.env['account.invoice'].search(
            [('state', '=', 'open'), ('type', '=', 'out_invoice'), ('date_due', '<=', self.date)])
        p_ids = []
        if not partners:
            raise RedirectWarning('No Due Customers')
        for p_id in partners:
            if p_id.partner_id.parent_id.id not in p_ids and p_id.partner_id.parent_id.id:
                p_ids.append(p_id.partner_id.parent_id.id)
            if p_id.partner_id.id not in p_ids and not p_id.partner_id.parent_id.id:
                p_ids.append(p_id.partner_id.id)

        data = {
            'date': self.date,
        }
        return self.env['report'].get_action(p_ids, 'account.report_overdue', data)

    def show_customer(self):
        partners = self.env['account.invoice'].search(
            [('state', '=', 'open'), ('type', '=', 'out_invoice'), ('date_due', '<=', self.date)])
        p_ids = []
        if not partners:
            raise RedirectWarning('No Due Customers')
        compose_form = self.env.ref(
            'account_customer_overdue_drc.overdue_customer_wizard_form_view', False)
        return {
            'name': ('Print/send overdue customer report'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail_overdue_payment_wizard',
            'view_id': compose_form.id,
            'target': 'new',

        }


class Wizard(models.TransientModel):
    _name = 'mail_overdue_payment_wizard'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _get_overdue_partners(self):
        wizard_obj = self.env['wizard_overdue'].search(
            [], limit=1, order='id desc')
        partners = self.env['account.invoice'].search(
            [('state', '=', 'open'), ('type', '=', 'out_invoice'), ('date_due', '<=', wizard_obj.date)])

        partners_list = []
        for p_id in partners:
            if p_id.partner_id.parent_id.id not in partners_list and p_id.partner_id.parent_id.id:
                partners_list.append(p_id.partner_id.parent_id.id)
            if p_id.partner_id.id not in partners_list and not p_id.partner_id.parent_id.id:
                partners_list.append(p_id.partner_id.id)
        return partners_list[:]

    res = fields.Many2many(
        'res.partner', string="Partners", default=_get_overdue_partners, domain="[('customer', '=', True),('company_type', '=','company')]")

    def print_report(self, data):
        wizard_obj = self.env['wizard_overdue'].search(
            [], limit=1, order='id desc')
        data = {
            'date':  wizard_obj.date, }
        return self.env['report'].get_action(self.res.ids, 'account.report_overdue', data=data)

    def send_email(self):
        template_id = self.env.ref(
            'account_customer_overdue_drc.mass_mail_account_overdue_template')
        user = self.env.user.email
        wizard_obj = self.env['wizard_overdue'].search(
            [], limit=1, order='id desc')

        for partner in self.res:
            po_obj = self.env['res.partner'].browse(partner.id)
            ctx = dict(
                overdue_partner=po_obj,
                sender=user,
                date=wizard_obj.date)
            self.env['mail.template'].with_context(ctx).browse(
                template_id.id).send_mail(partner.id, force_send=True)