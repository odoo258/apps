# -*- coding: utf-8 -*-
{
    'name': "Import Stock Inventory from Excel/CSV File",

    'summary': """
        stock inventory import from excel or csv file""",

    'description': """
        Import inventory menu open Wizard and import excel or csv file 
        then create inventory and products are listed in inventory details 
        products are in excel or csv file data.
        Menu: Inventory/Inventory Control/Import Inventory
    """,

    'author': "DRC systems India Pvt. Ltd",
    'website': "http://www.drcsystems.com/",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['sale', 'stock','purchase'],
    'sequence': 1,

    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_inventory_view.xml',
    ],

    'installable': True,
    "auto_install": False,
    "active": True
}
