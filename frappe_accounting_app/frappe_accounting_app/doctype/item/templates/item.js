
function on_add_to_cart_click() {
    frappe.call({
        method: "frappe_accounting_app.frappe_accounting_app.doctype.cart.cart.add_item_to_cart",
        args: {
            "item_name": '{{ doc.item_name }}',
        }
    })
}

function on_view_cart_click() {
    console.log('view cart clicked {{ doc.item_name }}')
}

