# -*- coding: utf-8 -*-

{
    'name': 'Accounting Customer/Supplier Statement',
    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com",
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'views/account_customer_statement_view.xml',
        'wizard/inherited_account_report_partner_ledger_view.xml'
    ],
    'installable': True,
    'application': False
}
