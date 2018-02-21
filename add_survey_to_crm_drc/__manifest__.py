# -*- coding: utf-8 -*-
{
    'name': "Add survey to CRM",

    'summary': """Adds survey to CRM.""",

    'description': """
       This module provides facility to take survey of users depending on project's stage.""",

    'author': "DRC Systems India Pvt. Ltd",
    'website': "http://www.drcsystems.com/",

    'category': 'Marketing',
    'version': '1.0',

    'images': ['static/description/icon.png',
               'static/description/add_survey_crm1.png',
               'static/description/add_survey_crm2.png',
               'static/description/add_survey_crm3.png',
               'static/description/add_survey_crm4.png',
               'static/description/add_survey_crm5.png',
               'static/description/add_survey_crm6.png',
               'static/description/add_survey_crm7.png',
               'static/description/add_survey_crm8.png',
               ],

    'depends': ['sale', 'survey_crm'],

    'data': [
        'views/add_survey_to_crm.xml',
        'views/survey_crm_templates.xml'
    ],

    "demo_xml": ['data/demo.xml'],

    'installable': True,
    "auto_install": False,
    "active": True
}
