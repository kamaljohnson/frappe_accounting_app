# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class JournalEntry(Document):

	def before_save(self):
		""" 
		1. Checks if total credits is equal to total debits | throws error msg 
		2. Updates the total_credits and total_debits
		"""
		
		self.total_debit = 0
		self.total_credit = 0
		
		for accounting_entry in self.get('accounting_entries'):
			self.total_credit += accounting_entry.credit
			self.total_debit += accounting_entry.debit

		if self.total_credit != self.total_debit:
			frappe.throw(_('Total credit should be equal to total debit'))

	def on_submit(self):
		"""
		1. Creates all the Ledger entries curresponding to each accounting entry
		2. Set corresponding fiscal year for each ledger entries
		"""

		fiscal_year = frappe.get_all(
			'Fiscal Year',
			filters = {
				'from_date': ['<=', self.posting_date],
				'to_date': ['>=', self.posting_date]
			},
			pluck = 'name'
		)

		for accounting_entry in self.get('accounting_entries'):
			ledger_entry_doc = frappe.get_doc({
				'doctype': 'Ledger Entry',
				'posting_date': self.posting_date,
				'account': accounting_entry.account,
				'debit': accounting_entry.debit,
				'credit': accounting_entry.credit,
				'voucher_type': 'Journal Entry',
				'voucher_number': self.name,
				'fiscal_year': fiscal_year[0],
				'company': self.company
			})
			ledger_entry_doc.insert()
		