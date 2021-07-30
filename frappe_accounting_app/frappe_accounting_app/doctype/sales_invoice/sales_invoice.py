# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document

class SalesInvoice(Document):
	
	def before_save(self):
		"""
		1. Compute amount field for each sales invoice item
		2. Calculate the grand_total
		"""
		
		grand_total = 0

		for sales_invoice_item in self.get('items'):
			amount = flt(sales_invoice_item.rate) * sales_invoice_item.quantity
			sales_invoice_item.amount = amount
			grand_total += amount

		self.grand_total = grand_total

	
	def on_submit(self):
		"""
		1. Set fiscal year for ledger entries
		2. Create ledger entries
		"""

		sales_accounts = frappe.get_all(
			'Account',
			filters = {
				'account_type': ['=', 'Income']
			},
			pluck = 'name'
		)

		debtors_accounts = frappe.get_all(
			'Account',
			filters = {
				'account_type': ['=', 'Receivable']
			},
			pluck = 'name'
		)

		if len(sales_accounts) == 0:
			frappe.throw(_('There is no income account set'))
			return
		if len(debtors_accounts) == 0:
			frappe.throw(_('There is no receivable account set'))
			return

		sales_account = sales_accounts[0]
		debtors_account = debtors_accounts[0]

		ledger_entry_doc1 = frappe.get_doc({
			'doctype': 'Ledger Entry',
			'posting_date': self.posting_date,
			'account': sales_account,
			'debit': self.grand_total,
			'credit': 0,
			'voucher_type': 'Sales Invoice',
			'voucher_number': self.name,
			'company': self.company
		})

		ledger_entry_doc2 = frappe.get_doc({
			'doctype': 'Ledger Entry',
			'posting_date': self.posting_date,
			'account': debtors_account,
			'debit': 0,
			'credit': self.grand_total,
			'voucher_type': 'Sales Invoice',
			'voucher_number': self.name,
			'company': self.company
		})

		ledger_entry_doc1.insert()
		ledger_entry_doc2.insert()