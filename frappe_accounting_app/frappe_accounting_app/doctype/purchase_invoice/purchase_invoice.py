# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document

class PurchaseInvoice(Document):

	def before_save(self):
		"""
		1. Compute amount field for each purhcase invoice item
		2. Calculate the grand_total
		"""
		
		grand_total = 0

		for purchase_invoice_item in self.get('items'):
			purchase_invoice_item_doc = frappe.get_doc(purchase_invoice_item)	
			amount = flt(purchase_invoice_item_doc.rate) * purchase_invoice_item_doc.quantity
			purchase_invoice_item_doc.amount = amount
			grand_total += amount

		self.grand_total = grand_total