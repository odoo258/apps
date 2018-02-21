
{
    'name': 'Odoo Professional Report Templates',
    'version': '1.0',
    
    'category': 'Tools',
    
    'author': 'DRC',
   
    'depends': ['web_widget_color', 'account' ],
    'data': [
		"views/res_company.xml",
		"invoice_report/multiple_invoice_report_view.xml",
        # "invoice_report/fency_report_account.xml",
		"invoice_report/report_invoice_creative.xml",
        "invoice_report/report_invoice_elegant.xml",
		"invoice_report/report_invoice_contemprory.xml",
        "invoice_report/report_invoice_exclusive.xml",
        "invoice_report/report_invoice_professional.xml",
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}
