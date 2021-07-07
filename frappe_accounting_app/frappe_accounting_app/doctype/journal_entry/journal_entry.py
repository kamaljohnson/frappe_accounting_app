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

	# TODO: on_submit(): check if total_debt = total_credits
	def on_submit(self):
		pass