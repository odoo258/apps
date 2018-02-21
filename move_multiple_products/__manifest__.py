# -*- coding: utf-8 -*-
{
    'name': "Move Multiple Products",

    'summary': """
        Move Multiple Products At Once""",

    'description': """
       Move Multiple Products At Once.
    """,

    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com/",
    'category': 'Warehouse',
    'version': '0.1',
    'depends': ['stock','purchase'],
    'images': ['static/description/move_multiple.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/scrap_workflow.xml'
    ],
    'currency': 'EUR',
    'installble': True,
    'auto_install': False,
    'application': False,
    'price': 15,
}
