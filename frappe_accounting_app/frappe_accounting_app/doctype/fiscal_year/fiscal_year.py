# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class FiscalYear(Document):

	def before_save(self):
		"""
		1. Check if from_date to to_date lies inside any exsisting fiscal years
		2. Else proceed to save the fiscal year
		"""

		if self.from_date < self.to_date:
			if not self.validate_overlaps():
				frappe.throw(_('Fiscal year overlapping with existing one'))
		else:
			frappe.throw(_('from_date should be before to_date'))

	def validate_overlaps(self):

		overlapping_fiscal_years = frappe.get_all(
			'Fiscal Year',
			filters={
				'from_date': ['<=', self.from_date],
				'to_date': ['>=', self.from_date],
				'name': ['!=', self.name]
			}
		)

		overlapping_fiscal_years += frappe.get_all(
			'Fiscal Year',
			filters={
				'from_date': ['<=', self.to_date],
				'to_date': ['>=', self.to_date],
				'name': ['!=', self.name]
			}
		)

		overlapping_fiscal_years += frappe.get_all(
			'Fiscal Year',
			filters={
				'from_date': ['>=', self.from_date],
				'to_date': ['<=', self.to_date],
				'name': ['!=', self.name]
			}
		)

		return len(overlapping_fiscal_years) == 0