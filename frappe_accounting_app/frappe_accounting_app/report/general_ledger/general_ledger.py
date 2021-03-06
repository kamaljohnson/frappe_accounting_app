# Copyright (c) 2013, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

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
			'fieldname': 'voucher_type',
			'label': _('Voucher Type'),
			'fieldtype': 'Link',
			'options': 'DocType',
			'width': 200
		},
		{
			'fieldname': 'voucher_number',
			'label': _('Voucher No'),
			'fieldtype': 'Dynamic Link',
			'options': 'voucher_type',
			'width': 200
		}
		,
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

def get_data(filters=None) -> list:
	"""
	1. Get all ledger entries
	2. Generate data according to layout
	"""
	data = []

	if 'from_date' in filters and 'to_date' in filters:
		if filters['from_date'] > filters['to_date']:
			frappe.throw(_('from_date should be less than to_date'))
			return data

		filters['posting_date'] = ['>=', filters.pop('from_date')]
		filters['posting_date'] = ['<=', filters.pop('to_date')]

	if 'account' in filters:
		filters['account'] = ['in', filters.pop('account')]

	for ledger_entry in frappe.get_all(
			'Ledger Entry',
			filters=filters,
			fields=[
				'account',
				'posting_date',
				'credit',
				'debit',
				'voucher_type',
				'voucher_number'
			]
	):
		data.append({
			'account': ledger_entry.account,
			'posting_date': ledger_entry.posting_date,
			'voucher_type': ledger_entry.voucher_type,
			'voucher_number': ledger_entry.voucher_number,
			'credit': ledger_entry.credit,
			'debit': ledger_entry.debit
		})

	return data
