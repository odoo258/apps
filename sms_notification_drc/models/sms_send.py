# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SendSms(models.Model):
    _name = "send.sms"
    _rec_name = 'send_sms_to'

    sms_state = fields.Selection(
        [('draft', 'Draft'), ('sent', 'Sent')], default="draft")
    send_sms_to = fields.Selection([('group', 'Group'), ('multiple members', 'Multiple members'), (
        'individual member', 'Individual Member/Number')], string="Send SMS to:")
    recipients = fields.Many2many('res.partner', string="Recipients")
    recipient_id = fields.Many2one('res.partner', string="Recipient")
    sms_group_id = fields.Many2one('group.sms', string="Group")
    sms_gateway_send_sms = fields.Many2one(
        'gateway.configuration', string="SMS Gateway")
    sms_to = fields.Char(string="To", required=True)
    sms_auto_delete = fields.Boolean(string="Auto Delete", default=True)
    sms_template_id = fields.Many2one('template.sms', string="Template")
    sms_message = fields.Text(
        string="Message", required=True)
    delivery_ids = fields.One2many(
        'delivery.report', 'delivery_id', store=True, index=True)

    @api.onchange('sms_template_id')
    def onchange_template(self):
        """Returns message of selected template"""
        self.sms_message = self.sms_template_id.content

    @api.onchange('recipients', 'sms_group_id', 'recipient_id')
    def onchange_recipients(self):
        """Returns recipient contact number"""
        self.ensure_one()
        multiple_members, group_members = [], []
        if self.send_sms_to == 'multiple members':
            if not self.env['res.users'].has_group('sms_notification_drc.group_country_call'):
                for records in self.recipients:
                    if records.mobile.startswith('+'):
                        multiple_members.append(int(records.mobile))
                    elif records.country_id:
                        multiple_members.append(int((
                            str(records.country_id.phone_code) + str(records.mobile))))
                    else:
                        multiple_members.append(int((
                            str(records.company_id.country_id.phone_code) + str(records.mobile))))
                    self.sms_to = multiple_members
                    self.sms_to = str(multiple_members).replace(
                        '[', '+').replace(']', '').replace(',', '<+')
        elif self.send_sms_to == 'group':
            for records in self.sms_group_id.member_ids:
                group_members.append(int(records.group_mobile))
                self.sms_to = str(group_members).replace(
                    '[', '+').replace(']', '').replace(',', '<+')
        elif self.send_sms_to == 'individual member':
            self.sms_to = self.recipient_id.mobile

    def draft_sms(self):
        self.sms_state == 'draft'
