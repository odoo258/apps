# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GroupSms(models.Model):
    _name = "group.sms"
    _rec_name = 'group_name'

    group_name = fields.Char(string="Group Name", required=True)
    total_member = fields.Integer(
        string="Total members", compute='compute_total_member')
    member_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Supplier'), (
        'any', 'Any')], string="Member Type", required=True)
    member_ids = fields.One2many('group.users', 'member_id')

    @api.one
    def compute_total_member(self):
        """Returns total members"""
        self.total_member = len(self.member_ids)


class GroupUsers(models.Model):
    _name = "group.users"

    group_partner_id = fields.Many2one('res.partner', string="Name")
    group_mobile = fields.Char(related='group_partner_id.mobile')
    group_email = fields.Char(related='group_partner_id.email')
    member_id = fields.Many2one('group.sms')
