# -*- coding: utf-8 -*-
{
    'name': "SMS Notification",

    'summary': """This module provides facility to send SMS notification to the mobile number.""",

    'description': """
       This module provides facility to send SMS notification to the mobile number,user can view delivery report and can send sms using template.
    """,

    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com/",

    'category': 'Service',
    'version': '1.0',

    'images': ['static/description/banner.jpg',
               ],

    'depends': ['sale'],

    'data': [
        'security/sms_notification_security.xml',
        'views/base_config_settings.xml',
        'views/sms_gateway_configuration.xml',
        'views/sms_send.xml',
        'views/sms_group.xml',
        'views/sms_report.xml',
        'views/sms_template.xml',
    ],

    "demo": ['data/demo.xml'],

    'installable': True,
    "auto_install": False,
    "active": True
}
