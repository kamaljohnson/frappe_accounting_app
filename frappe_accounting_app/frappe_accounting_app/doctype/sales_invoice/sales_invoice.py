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
			sales_invoice_item_doc = frappe.get_doc(sales_invoice_item)	
			amount = flt(sales_invoice_item_doc.rate) * sales_invoice_item_doc.quantity
			sales_invoice_item_doc.amount = amount
			grand_total += amount

		self.grand_total = grand_total