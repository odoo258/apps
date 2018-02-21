from odoo.addons.account.tests.test_reconciliation import TestReconciliation
import time

class TestReconciliation1(TestReconciliation):
    # def setUp(self):

    def test_reconcile_bank_statement_with_payment_and_writeoff(self):
        super(TestReconciliation1,self).test_reconcile_bank_statement_with_payment_and_writeoff()
        self.currency_usd_id = self.env.ref("base.USD").id
        self.partner_agrolait_id = self.env.ref("base.res_partner_2").id
        self.bank_journal_usd = self.env['account.journal'].create({'name': 'Bank US', 'type': 'bank', 'code': 'BNK68', 'currency_id': self.currency_usd_id})
        invoice = self.create_invoice(type='out_invoice', invoice_amount=80, currency_id=self.currency_usd_id)
        # register payment on invoice
        payment = self.env['account.payment'].create({'payment_type': 'inbound',
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'partner_type': 'customer',
            'partner_id': self.partner_agrolait_id,
            'amount': 80,
            'currency_id': self.currency_usd_id,
            'payment_date': time.strftime('%Y') + '-07-15',
            'journal_id': self.bank_journal_usd.id,
            'cash_reg_entry': True,
            })
        payment.post()
        print "00000000000000000000000000000000000000000000000000000000000000"
        # payment_move_line = False
        # bank_move_line = False
        # for l in payment.move_line_ids:
        #     if l.account_id.id == self.account_rcv.id:
        #         payment_move_line = l
        #     else:
        #         bank_move_line = l
        # invoice.register_payment(payment_move_line)

        # # create bank statement
        # bank_stmt = self.acc_bank_stmt_model.create({
        #     'journal_id': self.bank_journal_usd.id,
        #     'date': time.strftime('%Y') + '-07-15',
        # })

        # bank_stmt_line = self.acc_bank_stmt_line_model.create({'name': 'payment',
        #     'statement_id': bank_stmt.id,
        #     'partner_id': self.partner_agrolait_id,
        #     'amount': 85,
        #     'date': time.strftime('%Y') + '-07-15',})

        # #reconcile the statement with invoice and put remaining in another account
        # bank_stmt_line.process_reconciliation(payment_aml_rec= bank_move_line, new_aml_dicts=[{
        #     'account_id': self.diff_income_account.id,
        #     'debit': 0,
        #     'credit': 5,
        #     'name': 'bank fees',
        #     }])

        # # Check that move lines associated to bank_statement are correct
        # bank_stmt_aml = self.env['account.move.line'].search([('statement_id', '=', bank_stmt.id)])
        # bank_stmt_aml |= bank_stmt_aml.mapped('move_id').mapped('line_ids')
        # self.assertEquals(len(bank_stmt_aml), 4, "The bank statement should have 4 moves lines")
        # lines = {
        #     self.account_usd.id: [
        #         {'debit': 3.27, 'credit': 0.0, 'amount_currency': 5, 'currency_id': self.currency_usd_id},
        #         {'debit': 52.33, 'credit': 0, 'amount_currency': 80, 'currency_id': self.currency_usd_id}
        #         ],
        #     self.diff_income_account.id: {'debit': 0.0, 'credit': 3.27, 'amount_currency': -5, 'currency_id': self.currency_usd_id},
        #     self.account_rcv.id: {'debit': 0.0, 'credit': 52.33, 'amount_currency': -80, 'currency_id': self.currency_usd_id},
        # }
        # for aml in bank_stmt_aml:
        #     line = lines[aml.account_id.id]
        #     if type(line) == list:
        #         # find correct line inside the list
        #         if line[0]['debit'] == round(aml.debit, 2):
        #             line = line[0]
        #         else:
        #             line = line[1]
        #     self.assertEquals(round(aml.debit, 2), line['debit'])
        #     self.assertEquals(round(aml.credit, 2), line['credit'])
        #     self.assertEquals(round(aml.amount_currency, 2), line['amount_currency'])
        #     self.assertEquals(aml.currency_id.id, line['currency_id'])
        
