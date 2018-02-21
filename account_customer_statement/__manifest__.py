# -*- coding: utf-8 -*-
{
    'name': "account_customer_statement",

    'summary': """ Print Customer/Supplier Statements""",
    'description': """
        Print Customer/Supplier Statements
    """,
    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/account_customer_statement_view.xml',
    ],
    # only loaded in demonstration mode
    
}