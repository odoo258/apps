# -*- coding: utf-8 -*-
from odoo import fields, models


class GatewayConfiguration(models.Model):
    _name = "gateway.configuration"
    _rec_name = 'description'

    description = fields.Char(string="Description", required=True)
    priority = fields.Integer(string="Priority")
    mobile = fields.Char(string="Mobile No.", required=True)
    sms_gateway = fields.Selection([], string="SMS Gateway")
