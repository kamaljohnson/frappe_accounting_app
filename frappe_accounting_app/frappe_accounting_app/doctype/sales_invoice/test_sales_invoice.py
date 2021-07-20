# Copyright (c) 2021, Kamal Johnson and Contributors
# See license.txt

import frappe
import unittest
from datetime import datetime
from frappe.utils import flt

def create_dummy_sales_invoice():
	print('creating sales invoice')

	sales_invoice_items = []

	items = frappe.get_all('Item', fields=['name', 'standard_selling_rate'])[0:2]		# getting 3 items from item list

	total_amount = 0.0

	for item in items:
		print('Item: {}'.format(item))
		quantity = 1
		sales_invoice_item = frappe.get_doc({
			'doctype': 'Sales Invoice Item',
			'item': item.name,
			'quantity': quantity
		})
		sales_invoice_items.append(sales_invoice_item)
		total_amount += quantity * item.standard_selling_rate

	sales_invoice = frappe.get_doc({
		'doctype': 'Sales Invoice',
		'company': 'Gada Electronics',
		'customer': 'Administrator',
		'posting_date': datetime.now().date(),
		'items': sales_invoice_items
	})

	sales_invoice.insert()
	sales_invoice.submit()

	return (sales_invoice.name, total_amount)

class TestSalesInvoice(unittest.TestCase):
	def tearDown(self):
		frappe.db.rollback()

	def test_ledger_entries(self):
		print('testing ledger entries')

		ledger_entries_before_test = frappe.db.count('Ledger Entry')
		print('before count: {}'.format(ledger_entries_before_test))

		create_dummy_sales_invoice()

		ledger_entries_after_test = frappe.db.count('Ledger Entry')
		print('after count: {}'.format(ledger_entries_after_test))

		ledger_entries_created = ledger_entries_after_test - ledger_entries_before_test
		self.assertEqual(ledger_entries_created, 2, "Expected 2 ledger entries for each sales invoice. but created: {}".format(ledger_entries_created))

	def test_sales_invoice_total(self):
		print('testing sales invoice total')

		sales_invoice_name, expected_total_amount = create_dummy_sales_invoice()
		sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)

		self.assertEqual(flt(sales_invoice.grand_total), expected_total_amount, "Expected {} as total but sales invoice total is {}".format(flt(sales_invoice.grand_total), expected_total_amount))
