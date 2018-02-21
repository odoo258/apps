# -*- coding: utf-8 -*-
from odoo import fields, models


class DeliveryReport(models.Model):
    _name = "delivery.report"
    _rec_name = 'sms_to_delivery'

    sms_state_delivery = fields.Selection(
        [('outgoing', 'Outgoing'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered')], default="draft")
    sms_gateway_send_sms_delivery = fields.Many2one(
        'gateway.configuration', string="SMS Gateway")
    delivery_id = fields.Many2one('send.sms')
    sms_to_delivery = fields.Char(string="To")
    sms_auto_delete_delivery = fields.Boolean(string="Auto Delete")
    sms_message_delivery = fields.Text(
        string="Message", required=True)
