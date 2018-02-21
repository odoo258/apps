# -*- coding: utf-8 -*-
import logging
from odoo.addons.crm.tests.common import TestCrm
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestAddSurvey(TestCrm):

    def test_00_add_survey(self):

        crm1 = self.env['crm.lead'].create({
            'survey_id': 9,
            'name': 'Demo',
        })
        logger.info('Create Crm Lead')

        crm1.action_start_survey()
        logger.info('Start Survey')

        self.env['crm.stage'].create({
            'name': 'Demo',
            'survey': 9
        })
        logger.info('Create crm stage')

        self.env['survey.user_input'].create({
            'survey_id': 9,
            'survey_input_id': 1
        })
        logger.info('Create survey input')
