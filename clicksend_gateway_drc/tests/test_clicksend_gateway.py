# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestClicksendGateway(TransactionCase):

    def test_00_clicksend_gateway(self):

        sms1 = self.env['gateway.configuration']
        sms1.test_connection()
        logger.info('Clicksend Test Connection')

        sms2 = self.env['send.sms']
        sms2.send_sms()
        logger.info('Clicksend Send SMS')
