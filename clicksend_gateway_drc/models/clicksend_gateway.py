# -*- coding: utf-8 -*-
import json
import requests
import base64
import urllib2
from urllib2 import Request, urlopen
from odoo.exceptions import UserError, Warning
from odoo.tools import ustr
from datetime import date
from odoo import api, fields, models, _


class ClicksendConfig(models.Model):
    _inherit = 'gateway.configuration'

    clicksend_username = fields.Char(
        string="Clicksend Username", required=True)
    clicksend_password = fields.Char(
        string="Clicksend Password", required=True)
    clicksend_api_key = fields.Char(string="Clicksend Api Key", required=True)
    sms_gateway = fields.Selection(
        selection_add=[('clicksend', 'Clicksend')], required=True)

    @api.one
    def test_connection(self):
        """Tests the connection of selected gateway"""
        msg = (self.clicksend_username or '') + \
            ':' + (self.clicksend_password or '')
        encode_message = base64.b64encode(msg.encode("utf-8"))
        authorization = "Basic" + ' ' + encode_message
        parse_data = {
            'messages': [{
                'body': 'Clicksend Test Connection Successful...',
                'source': 'Python',
                'to': self.mobile
            }]
        }
        headers = {
            'Content-Type': 'application/json;',
            'Authorization': authorization
        }
        resp = requests.post(
            'https://rest.clicksend.com/v3/sms/send', data=json.dumps(parse_data), headers=headers)
        response_body = resp.json()
        if response_body['response_code'] == "SUCCESS":
            raise Warning(
                _("Test Connection status has been sent on: '%s'") % self.mobile)
        else:
            raise UserError(
                _("SMS sent failed!"))


class ClicksendSend(models.Model):
    _inherit = 'send.sms'

    @api.one
    def try_sms(self):
        """Returns entry of message success"""
        success_entry = {
            'sms_to_delivery': self.sms_to,
            'sms_gateway_send_sms_delivery': self.sms_gateway_send_sms.id,
            'sms_state_delivery': "sent",
            'sms_message_delivery': self.sms_message,
        }
        self.delivery_ids = [(0, 0, success_entry)]

    @api.one
    def except_sms(self):
        """Returns entry of message error"""
        error_entry = {
            'sms_to_delivery': self.sms_to,
            'sms_gateway_send_sms_delivery': self.sms_gateway_send_sms.id,
            'sms_state_delivery': "undelivered",
            'sms_message_delivery': self.sms_message,
        }
        self.delivery_ids = [(0, 0, error_entry)]

    def authorization_sms(self):
        msg = (self.sms_gateway_send_sms.clicksend_username or '') + \
            ':' + (self.sms_gateway_send_sms.clicksend_password or '')
        encode_message = base64.b64encode(msg.encode("utf-8"))
        authorization = "Basic" + ' ' + encode_message
        return authorization

    @api.one
    def send_sms(self):
        """Sends message to the number of members selected"""
        if self.send_sms_to == 'individual member':
            parse_data = {
                'messages': [{
                    'body': self.sms_message,
                    'source': 'Python',
                    'to': self.recipient.mobile,
                }]
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.authorization_sms()
            }
            resp = requests.post(
                'https://rest.clicksend.com/v3/sms/send', data=json.dumps(parse_data), headers=headers)
            response_body = resp.json()
            print response_body
            # import pdb;pdb.set_trace()
            if response_body['response_code'] == "SUCCESS":
                self.sms_id = response_body['data'][
                    'messages'][0]['message_id']
                self.try_sms()
                self.sms_state = 'sent'
            else:
                self.except_sms()
                self.sms_state = 'sent'
                # raise UserError(
                #     _("SMS sent failed!"))
        elif self.send_sms_to == 'multiple members' or 'group':
            abc = {
                "list_name": "14-12-2017",
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.authorization_sms()
            }
            request1 = requests.post(
                'https://rest.clicksend.com/v3/lists', data=json.dumps(abc), headers=headers)
            response_body = request1.json()
            if response_body['response_code'] == "SUCCESS":
                for records in self.sms_to.split('<'):
                    values = {
                        "phone_number": records,
                    }
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': self.authorization_sms()
                    }
                    print response_body.get('data').get('list_id')
                    request = requests.post('https://rest.clicksend.com/v3/lists/%d/contacts' %
                                            int(response_body.get('data').get('list_id')), data=json.dumps(values), headers=headers)
                    response_body = request.json()
                if response_body['response_code'] == "SUCCESS":
                    data = {
                        'messages': [{
                            'body': self.sms_message,
                            'source': 'Python',
                            'list_id': response_body['data']['list_id']
                        }]
                    }
                    headers = {
                        'Content-Type': 'application/json;',
                        'Authorization': self.authorization_sms()
                    }
                    resp = requests.post(
                        'https://rest.clicksend.com/v3/sms/send', data=json.dumps(data), headers=headers)
                    response_body = resp.json()
                    if response_body['response_code'] == "SUCCESS":
                        self.sms_id = response_body['data'][
                            'messages'][0]['message_id']
                        self.try_sms()
                        self.sms_state = 'sent'
            else:
                self.sms_state = 'sent'
                self.except_sms()
        self.search([('sms_auto_delete', '=', 'True')]).unlink()


class SaleOrdersms(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        """Sends the message when sale order is confirmed"""
        res = super(SaleOrdersms, self).action_confirm()
        gateway = self.env['gateway.configuration'].search(
            [('sms_gateway', '=', 'clicksend')])
        template = self.env['template.sms'].search(
            [('template_condition', '=', ['order_confirm'])])
        if template:
            dst = self.partner_id.mobile
            parse_data = {
                'messages': [{
                    'body': template.content,
                    'source': 'Python',
                    'to': dst,
                }]
            }
            msg = (gateway.clicksend_username or '') + \
                ':' + (gateway.clicksend_password or '')
            authorization = "Basic" + ' ' + \
                base64.b64encode(msg.encode("utf-8"))
            headers = {
                'Content-Type': 'application/json',
                'Authorization': authorization
            }
            try:
                response = requests.post(
                    'https://rest.clicksend.com/v3/sms/send', data=json.dumps(parse_data), headers=headers)
                response_body = response.json()
            except Exception as e:
                raise UserError(_("Error in sending SMS:\n %s") % ustr(e))
        return res
