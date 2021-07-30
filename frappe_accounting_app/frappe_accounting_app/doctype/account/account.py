# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet

class Account(NestedSet):

	def before_save(self):
		if self.account_type in ['Income', 'Liability', 'Payable']:
			self.balance_type = 'Credit'
		elif self.account_type in ['Asset', 'Expense', 'Receivable']:
			self.balance_type = 'Debit'
		else:
			frappe.throw(_('Account type not found'))