# Copyright (c) 2013, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data()

	return columns, data

def get_columns() -> list:
	columns = [
		{
			'fieldname': 'account',
			'label': _('Account'),
			'fieldtype': 'Link',
			'options': 'Account',
			'width': 200
		},
		{
			'fieldname': 'posting_date',
			'label': _('Posting Date'),
			'fieldtype': 'Date',
			'width': 200
		},
		{
			'fieldname': 'credit',
			'label': _('Credit'),
			'fieldtype': 'Currancy',
			'width': 200
		},
		{
			'fieldname': 'debit',
			'label': _('Debit'),
			'fieldtype': 'Currancy',
			'width': 200
		}
	]
	return columns

def get_data() -> list:
	"""
	1. Get all ledger entries
	2. Generate data according to layout
	"""
	data = []

	for ledger_entry in frappe.get_all(
		'Ledger Entry',
		fields=[
			'account',
			'posting_date',
			'credit',
			'debit'
		]
	):
		data.append({
			'account': ledger_entry.account,
			'posting_date': ledger_entry.posting_date,
			'credit': ledger_entry.credit,
			'debit': ledger_entry.debit
		})

	return data
