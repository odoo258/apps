# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSmsNotification(TransactionCase):

    def test_00_sms_notification(self):
        self.env['gateway.configuration'].create({
            'description': 'xyz',
            'mobile': 123456789
        })
        logger.info('create gateway configuration')

        self.env['group.sms'].create({
            'group_name': 'Group1',
            'total_member': 5,
            'member_type': 'customer'
        })
        logger.info('create Group SMS')

        self.env['delivery.report'].create({
            'sms_state_delivery': 'outgoing',
            'sms_to_delivery': '9876543212',
            'sms_message_delivery': 'Message delivered'
        })
        logger.info('Create Delivery Report')

        self.env['send.sms'].create({
            'sms_to': '9876543210',
            'sms_message': 'Hello'
        })
        logger.info('Send SMS')

        self.env['template.sms'].create({
            'template_name': 'Template1',
            'template_condition': 'order_confirm'
        })
        logger.info('SMS template')
