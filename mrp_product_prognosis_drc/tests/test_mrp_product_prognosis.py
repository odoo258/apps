# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, AccessError
from odoo.addons.product.tests.common import TestProductCommon
import logging


class TestMrpProductPrognosis(TestProductCommon):

    def test_00_mrp_product_prognosis(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        mrp1 = self.env['product.template'].create({
            'mrp_potential': 2.0,
            'bottleneck_component': 'xyz',
            'mrp_forecast': 1.0,
            'name': 'Demo'
        })
        logger.info('create product template')
