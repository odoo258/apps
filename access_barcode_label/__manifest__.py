# -*- coding: utf-8 -*-
{
    'name': 'Aaccess barcode label',
    'version': '0.1.0',
    'category': '',
    'summary': 'Report of selected products with selected fields ',
    'description': """
    Report of selected products with selected fields
    """,
    'author': 'DRC Systems India Pvt. Ltd.',
    'website': 'http://www.drcsystems.com/',
    'depends': ['sale', 'base'],
    'data': [
        'views/report_barcode_view.xml',
        'report/report_barcode.xml',
        'views/menu.xml',
    ],

    'application': False,
    'installable': True,
    'price':25,
    'currency' :'EUR',
}
