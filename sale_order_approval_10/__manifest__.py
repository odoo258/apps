# -*- coding: utf-8 -*-
{
    'name': 'Sales Order Double Validation',
    'version': '0.1.0',
    'category': '',
    'summary': 'Sales Approve ',
    'description': """
    Sales Order Double Validation
    """,
    'author': 'DRC Systems India Pvt. Ltd.',
    'website': 'http://www.drcsystems.com/',
    'depends': ['sale', 'base'],
    'data': [
        'views/credit_limit_view.xml',
        'views/sale_config_settings.xml',
    ],

    'application': False,
    'installable': True,
    'price':25,
    'currency' :'EUR',
}
