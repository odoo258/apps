# -*- coding: utf-8 -*-
{
    'name': "Mass Invoice Email Send",
    'summary': """mass invoice email send""",
    'description': """
        This module will send mass invoice mail to customer.
    """,
    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account', 'mail'],
    'data': [
        'wizard/mass_invoice_email_view.xml',
    ],
    'images': [
        'static/description/ms1.png',
        'static/description/ms2.png',
        'static/description/ms3.png',
    ],
}
