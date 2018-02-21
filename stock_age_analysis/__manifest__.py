# -*- coding: utf-8 -*-
{
    'name': 'Stock age analysis Report',
    'version': '0.1.0',
    'category': 'manufacturing',
    'summary': 'Stock age analysis report',
    'description': """
    Age analysis report of particular product or group can be downloaded
    """,
    'author': 'DRC Systems India Pvt. Ltd.',
    'website': 'http://www.drcsystems.com/',
    'depends': ['stock', 'base', 'account_accountant'],
    'images' : ['static/description/age_analysis_report.png'],
    'data': [
        'views/report_stock_age_analysis.xml',
        'wizard/stock_ageing.xml'
    ],

    'application': False,
    'installable': True,
    'price': 30,
    'currency':'EUR'
}
