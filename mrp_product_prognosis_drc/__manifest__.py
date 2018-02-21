{
    'name': "Mrp Product Prognosis",
    'summary': """This module is for the forecast of production,potential and bottleneck component of products.""",
    'category': 'Service',


    'version': '1.0',
    'application': False,

    'author': 'DRC Systems',
    'website': "http://www.drcsystems.com/",

    'depends': ['mrp','product','purchase'],
    'sequence': 1,


    # data files always loaded at installation
    'data': [
        'views/mrp_product_prognosis.xml',
    ],

    # data files containing optionally loaded demonstration data

    "demo_xml": [],
    "update_xml": [],

    'installable': True,
    "auto_install": False,
    "active": True

}
