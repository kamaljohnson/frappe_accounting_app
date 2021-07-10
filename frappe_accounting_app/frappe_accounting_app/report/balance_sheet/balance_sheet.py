# Copyright (c) 2013, Kamal Johnson and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of

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
			'width': 300
		},
		{
			'fieldname': 'amount',
			'label': _('Amount'),
			'fieldtype': 'Currency',
			'width': 300
		},
		{
			'fieldname': 'total',
			'label': _('Total'),
			'fieldtype': 'Currency',
			'width': 300
		}
	]
	return columns

def get_data() -> list:
	"""
	1. Get all assets and liability entries from the ledger
	2. Comput total assets / total libilities
	3. Generate data according to layout
	"""
	data = []

	# region Set assets using asset accounts from ledger entries
	total_assets = 0

	asset_accounts = get_descendants_of('Account', 'Application of Funds (Assets)')

	data.append({
		'indent': 0,
		'account': 'Assets'
	})

	for ledger_entry in frappe.get_all(
		'Ledger Entry',
		group_by='account',
		filters={
			'account': ['in', asset_accounts]
		},
		fields=[
			'account',
			'sum(credit) as amount'
		]
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.amount,
			'parent_account': 'Assets'
		})

		total_assets += ledger_entry.amount

	data.append({})
	data.append({
		'intend': 0,
		'account': 'Total Assets',
		'total': total_assets
	})
	data.append({})

	# endregion

	# region Set liabilities using liability accounts from ledger entries
	total_liabilities = 0

	liability_accounts = get_descendants_of('Account', 'Source of Funds (Liabilities)')

	data.append({
		'indent': 0,
		'account': 'Liabilities'
	})

	for ledger_entry in frappe.get_all(
			'Ledger Entry',
			group_by='account',
			filters={
				'account': ['in', liability_accounts]
			},
			fields=[
				'account',
				'sum(debit) as amount'
			]
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.amount,
			'parent_account': 'Liabilities'
		})

		total_liabilities += ledger_entry.amount

	data.append({})
	data.append({
		'intend': 0,
		'account': 'Total Liabilities',
		'total': total_liabilities
	})
	data.append({})

	# endregion

	return data
