# -*- coding: utf-8 -*-
from odoo import fields, models


class BaseConfig(models.TransientModel):
    _inherit = "base.config.settings"

    group_country_call = fields.Boolean(
        string="Are you managing country calling code with customer's mobile number?", implied_group='sms_notification_drc.group_country_call')
    module_plivo_gateway_drc = fields.Boolean(
        string="Install Plivo SMS Gateway")
    module_clicksend_gateway_drc = fields.Boolean(
        string="Install ClickSend SMS Gateway")
    module_twilio_gateway_drc = fields.Boolean(
        string="Install Twilio SMS Gateway")
