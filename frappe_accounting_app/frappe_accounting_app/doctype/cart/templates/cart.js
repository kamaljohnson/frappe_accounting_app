var api_req_headers = {
	'Content-Type': 'application/json',
};
if (window.csrf_token)
	api_req_headers['X-Frappe-CSRF-Token'] = window.csrf_token;

get_cart();

// used to validate all url fetch responses
function validateResponse(res) {
    if(res.ok) return res.json();
    else {
        console.log('an error occured while fetching url')
    }
}

function get_cart(cart) {
    cart_name = get_data('cartName')

    const options = {
		method: 'GET',
		headers: api_req_headers,
	};

    let url = document.location.origin + '/api/resource/Cart/' + cart_name;

    fetch(url, options).then(validateResponse).then(res => {
        cart = res.data;
        show_cart_items(cart.items);
    });
}

function show_cart_items(cart_items) {
    cart_items_doc = document.getElementById('cart_items');
    cart_items_doc.innerHTML = '';

    cart_items.forEach(cart_item => {
        var cart_item_slip_doc = document.createElement('DIV');
        cart_item_slip_doc.className = 'cart-item-slip';

        const options = {
            method: 'GET',
            headers: api_req_headers,
        };

        let url = document.location.origin + '/api/resource/Item/' + cart_item.item;

        fetch(url, options).then(validateResponse).then(res => {
            item = res.data;
            show_cart_item(item, cart_item.quantity, cart_item.amount, cart_item_slip_doc);
        });

        cart_items_doc.append(cart_item_slip_doc);
    });
}

function show_cart_item(item, quantity, amount, cart_item_slip_doc) {
    console.log('Item: ' + item.name + ' ' + quantity + ' ' + amount);
    cart_item_slip_doc.innerHTML = item.name;
}

function on_checkout_button_click() {

}

function get_data(key) {
    return $('#data_block').data()[key]
}