# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InvoiceDueList(models.TransientModel):
    _name = 'wizard.account_tax_report'
    _inherit = "account.common.report"

    @api.model
    def _get_account_report(self):
        reports = []
        if self._context.get('active_id'):
            menu = self.env['ir.ui.menu'].browse(self._context.get('active_id')).name
            reports = self.env['account.tax.report'].search([('name', 'ilike', menu)])
        return reports and reports[0] or False

    account_tax_report_id = fields.Many2one('account.tax.report', string='Account Reports', required=True, default=_get_account_report)
    detail = fields.Boolean('Display Details')
    # target_moves = fields.Selection([('all_entries', 'All Entries'), ('all_posted', 'All Posted Entries')], 'Target Moves', default='all_entries')

    def _print_report(self, data):
        data['form'].update(self.read(['date_from', 'date_to', 'account_tax_report_id', 'target_move', 'detail'])[0])
        return self.env['report'].get_action(self, 'account_tax_report_drc.report_tax', data=data)
