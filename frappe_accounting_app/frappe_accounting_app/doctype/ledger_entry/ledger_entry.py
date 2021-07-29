# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LedgerEntry(Document):

	# TODO: fetch fiscal year and set it using the posting date
	def before_save(self):
		fiscal_years = frappe.get_all(
			'Fiscal Year',
			filters = {
				'from_date': ['<=', self.posting_date],
				'to_date': ['>=', self.posting_date]
			},
			pluck = 'name'
		)

		if len(fiscal_years) != 0:
			self.fiscal_year = fiscal_years[0]
		else:
			frappe.throw(_('No fiscal year present, please add one'))