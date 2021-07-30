# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):
	columns =[
		{
			"fieldname" : "account",
			"label" : _("Account"),
			"fieldtype" : "Link",
			"options" : "Account",
			"width" : 300
		},
		{
			"fieldname" : "amount",
			"label" : _("Amount"),
			"fieldtype" : "Currency",
			"width" : 300
		},
		{
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"width": 300
		}
	]

	return columns

def get_data(filters):
	"""
	1. Get all income and expense entries from the ledger
	2. Compute profit / loss
	3. Generate data accourding to layout
	"""
	data = []

	# region Get income data using income accounts from ledger entries
	total_income = 0

	income_accounts = frappe.get_all(
		'Account',
		filters = {
			'balance_type': ['=', 'Credit'],
			'report_type': ['=', 'Profit and Loss']
		},
		pluck = 'name'
	)
	income_accounts.append("Income")

	data.append({
		'indent': 0,
		'account': 'Income',
	})

	for ledger_entry in frappe.get_all(
		'Ledger Entry',
		group_by='account',
		filters={
			'account': ['in', income_accounts]
		},
		fields=[
			'account',
			'sum(debit) as amount',
		]
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.amount,
			'parent_account': 'Income'
		})

		total_income += ledger_entry.amount

	data.append({})
	data.append({
		'intend': 0,
		'account': 'Total Income',
		'total': total_income
	})
	data.append({})

	# endregion

	# region Set expense data using expense account ledger entries
	total_expense = 0

	expense_accounts = frappe.get_all(
		'Account',
		filters = {
			'balance_type': ['=', 'Debit'],
			'report_type': ['=', 'Profit and Loss']
		},
		pluck = 'name'
	)
	expense_accounts.append("Expenses")

	data.append({
		'indent': 0,
		'account': 'Expenses'
	})

	for ledger_entry in frappe.get_all(
		'Ledger Entry',
		group_by='account',
		filters={
			'account': ['in', expense_accounts]
		},
		fields=[
			'account',
			'sum(credit) as amount',
		]
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.amount,
			'parent_account': 'Expenese'
		})

		total_expense += ledger_entry.amount

	data.append({})
	data.append({
		'intend': 0,
		'account': 'Total Expenses',
		'total': total_expense
	})
	data.append({})
	# endregion

	# region Compute profit / loss

	if total_income >= total_expense: 	# Profit
		net_profit = total_income - total_expense
		data.append({
			'account': 'Net Profit',
			'total': net_profit
		})
	else:								# Loss
		net_loss = total_expense - total_income
		data.append({
			'account': 'Net Loss',
			'total': net_loss
		})

	# endregion

	return data