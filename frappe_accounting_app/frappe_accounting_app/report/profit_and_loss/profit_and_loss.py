# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	# basic layout for P&L statement
	#	Sno	Account				Amount
	#	1	Income.
	#	2	 Indirect Sales		200
	# 	3	 Direct Sales		150
	# 		 ...income sources
	#	4	Total Income		350
	#	5	Expenses.
	#	6	 Indirect Expenses	50
	#	7	 Direct Expenses	100
	# 		 ...expense sources
	#	8	Total Expenses		150
	#	9	Net Profit			200

	return columns, data

def get_columns(filters):
	columns =[{
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
	}]

	return columns

def get_data(filters):
	data = []

	income_data = []
	expense_data = []

	total_income = 0
	total_expense = 0

	# [x] TODO: get all income accounts
	income_accounts = get_descendants_of("Account", "Income")
	income_accounts.append("Income")

	# [x] TODO: get all expense accounts
	expense_accounts = get_descendants_of("Account", "Expenses")
	expense_accounts.append("Expenses")

	# TODO: get ledger entries for all income accounts
	income_data.append({
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
		print('Account: {}'.format(ledger_entry.account))
		print('Amount: {}'.format(ledger_entry.amount))
		income_data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.amount,
		})

	# TODO: get ledger entries for all expense accounts
	expense_data.append({
		'indent': 0,
		'account': 'Expenses'
	})

	data = income_data + expense_data

	print('Data: {}'.format(data))

	# TODO: compute p/l
	if total_income >= total_expense: 	# Profit
		net_profit = total_income - total_expense
	else:								# Loss
		net_loss = total_expense - total_income

	return data