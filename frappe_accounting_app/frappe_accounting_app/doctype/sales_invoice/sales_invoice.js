// Copyright (c) 2021, Kamal Johnson and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Sales Invoice Item', {
    quantity: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        row.amount = row.quantity * row.rate;
        refresh_field('items');

        var grand_total = 0;
        for(let i = 0; i < frm.doc.items.length; i++) {
            grand_total += frm.doc.items[i].amount;
        }

        frm.doc.grand_total = grand_total;
        refresh_field('grand_total');
    }
})
