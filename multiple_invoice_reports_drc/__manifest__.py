
{
    'name': 'Custum Invoice Report Templates',
    'summary': """Invoice Report Templates""",
    'description': """
        this module will prints the custom invoice reports using multiple templates
    """,
    'author': "DRC Systems India Pvt. Ltd.",
    'website': "http://www.drcsystems.com",
    'category': 'Uncategorized',
    'depends': ['web_widget_color', 'account' ],
    'data': [
		"views/multiple_invoice_report_view.xml",
		"report/report_invoice_advanced.xml",
		"report/report_invoice_creative.xml",
        "report/report_invoice_elegant.xml",
		"report/report_invoice_contemprory.xml",
        "report/report_invoice_exclusive.xml",
        "report/report_invoice_professional.xml",
    ],
    'installable': True,
    'auto_install': False,
}
