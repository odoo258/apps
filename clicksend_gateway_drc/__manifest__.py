# -*- coding: utf-8 -*-
{
    'name': "Clicksend Gateway",

    'summary': """SMS Notification to employees""",

    'description': """
       This module provides facility to send SMS notification to the mobile number,user can view delivery report and can send sms using template.
    """,

    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com/",

    'category': 'Service',
    'version': '1.0',

    'images': ['static/description/banner.jpg',
               ],

    'depends': ['sms_notification_drc'],

    'data': [
        'views/clicksend_gateway.xml',
    ],

    'installable': True,
    "auto_install": False,
    "active": True
}
