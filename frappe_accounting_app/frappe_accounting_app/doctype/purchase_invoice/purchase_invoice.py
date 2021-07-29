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
            amount = flt(purchase_invoice_item.rate) * purchase_invoice_item.quantity
            purchase_invoice_item.amount = amount
            grand_total += amount

        self.grand_total = grand_total

    def on_submit(self):
        """
		1. Set fiscal year for ledger entries
		2. Create ledger entries
		"""

        ledger_entry_doc1 = frappe.get_doc({
            'doctype': 'Ledger Entry',
            'posting_date': self.posting_date,
            'account': 'Expenses',
            'debit': 0,
            'credit': self.grand_total,
            'voucher_type': 'Purchase Invoice',
            'voucher_number': self.name,
            'company': self.company
        })

        ledger_entry_doc2 = frappe.get_doc({
            'doctype': 'Ledger Entry',
            'posting_date': self.posting_date,
            'account': 'Creditors',
            'debit': self.grand_total,
            'credit': 0,
            'voucher_type': 'Purchase Invoice',
            'voucher_number': self.name,
            'company': self.company
        })

        ledger_entry_doc1.insert()
        ledger_entry_doc2.insert()
