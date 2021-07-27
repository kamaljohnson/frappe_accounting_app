// Copyright (c) 2016, Kamal Johnson and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [
        {
            'fieldname': 'posting_date',
            'label': __('Posting Date'),
            'fieldtype': 'Date',
            on_change: function() {
                frappe.query_report.set_filter_value('group_by', "Group by Voucher (Consolidated)");
            }
        },
        {
            'fieldname': 'voucher_number',
            'label': __('Voucher No'),
            'fieldtype': 'Data',
        }
	]
};
