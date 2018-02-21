
{
    'name': 'Odoo Professional Report Templates',
    'version': '1.0',
    'summary': 'Easily Customizable Report Template for Quotation/SO/Sales, Invoice, Picking/Delivery Order,RFQ/PO/Purchases',
    'category': 'Tools',
    'description': """
		Customize report, customize pdf report, customize template report, Customize Sales Order report,Customize Purchase Order report, Customize invoice report, Customize delivery Order report, Accounting Reports, Easy reports, Flexible report,Fancy Report template.
		
    """,
    'author': 'DRC',
    'website': 'http://www.browseinfo.in',
    'depends': ['web_widget_color', 'account' ],
    'data': [
		"res_company.xml",
		"invoice_report/fency_report_account.xml",
		"invoice_report/fency_report_invoice.xml",
		"invoice_report/report_invoice_classic.xml",
		"invoice_report/report_invoice_contemprory.xml",
"invoice_report/report_invoice_odoo_standard.xml"
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}
