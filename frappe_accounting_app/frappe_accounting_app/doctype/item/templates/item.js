var api_req_headers = {
	'Content-Type': 'application/json',
};
if (window.csrf_token)
	api_req_headers['X-Frappe-CSRF-Token'] = window.csrf_token;

set_customer_name();

// used to validate all url fetch responses
function validateResponse(res) {
    if(res.ok) return res.json();
    else {
        console.log('an error occured while fetching url')
    }
}

async function set_customer_name() {
    customer_name = 'not set';

    session_user = await get_user();

    let url = document.location.origin + '/api/resource/Customer/';
    url += '?filters=';
	url += '[["user", "=", "' + session_user + '"]]';

	const options = {
		method: 'GET',
		headers: api_req_headers,
	};

    fetch(url, options).then(validateResponse).then(res => {
        customers = res.data;
        if(customers.length == 1) {
            customer_name = customers[0].name;
            set_data('customerName', customer_name);
        } else {
            frappe.msgprint('Customer not set. please log in.');
        }
    });
}

function on_add_to_cart_click() {
    frappe.call({
        method: "frappe_accounting_app.frappe_accounting_app.doctype.cart.cart.add_item_to_cart",
        args: {
            "item_name": '{{ doc.item_name }}',
        }
    })
}

function on_view_cart_click() {
    customer_name = get_data('customerName');
    console.log('Customer: ' + customer_name);

    let url = document.location.origin + '/api/resource/Cart/';
    url += '?filters=';
	url += '[["customer", "=", "' + customer_name + '" ], ["status", "=", "Active"]]';

	const options = {
		method: 'GET',
		headers: api_req_headers,
	};

    fetch(url, options).then(validateResponse).then(res => {
        active_carts = res.data;
        if(active_carts.length != 0){
            active_cart = active_carts[0];
            window.location.href = "http://accounting.test:8000/carts/" + active_cart.name;
        } else {
            frappe.msgprint('Cart is empty, please add items to cart.');
        }
    });
}

async function get_user() {
    let url = document.location.origin + '/api/method/frappe.auth.get_logged_user';
	return fetch(url)
		.then(validateResponse)
		.then((res) => res.message);
}

function get_data(key) {
    return $('#data_block').data()[key];
}

function set_data(key, value) {
    $('#data_block').data()[key] = value;
}