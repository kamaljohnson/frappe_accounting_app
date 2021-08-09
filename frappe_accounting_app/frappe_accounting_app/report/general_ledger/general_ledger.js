// Copyright (c) 2016, Kamal Johnson and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [
        {
            'fieldname': 'voucher_number',
            'label': __('Voucher No'),
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'from_date',
            'label': __('From Date'),
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            'fieldtype': 'Date'
        },
        {
            'fieldname': 'to_date',
            'label': __('To Date'),
            "default": frappe.datetime.get_today(),
            'fieldtype': 'Date'
        },
        {
            'fieldname': 'account',
            'label': __('Account'),
            'fieldtype': 'MultiSelectList',
            'options': 'Account',
            get_data: function() {
				return frappe.db.get_link_options('Account');
			}
        }
	]
};
