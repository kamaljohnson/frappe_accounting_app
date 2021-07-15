var api_req_headers = {
	'Content-Type': 'application/json',
};
if (window.csrf_token)
	api_req_headers['X-Frappe-CSRF-Token'] = window.csrf_token;

// used to validate all url fetch responses
function validateResponse(res) {
    if(res.ok) return res.json();
    else {
        console.log('an error occured while fetching url')
    }
}

// handles input changes in search input and triggers search_text()
$('#search_input').each(function() {
   var elem = $(this);

   // Save current value of element
   elem.data('oldVal', elem.val());

   // Look for changes in the value
   elem.bind("propertychange change click keyup input paste", function(event){
      // If value has changed...
      if (elem.data('oldVal') != elem.val()) {
       // Updated stored value
       elem.data('oldVal', elem.val());

       search_text = document.getElementById('search_input').value
       search(search_text)
     }
   });
 });

async function search(search_text) {
    //  clear previous search results list
    let results_doc = document.getElementById('results');
    results_doc.innerHTML = '';

    if(search_text == '') return;

	const options = {
		method: 'GET',
		headers: api_req_headers,
	};

    let url = document.location.origin + '/api/resource/Item';
    url += '?fields=';
    url += '["name","image","standard_selling_rate"]';

    fetch(url, options).then(validateResponse).then(res => {
        items = res.data;
        result_items = get_search_results(items, search_text);
        show_search_results(result_items);
    });
}

function get_search_results(items, search_text) {
    result_items = [];
    search_text = search_text.toLowerCase();
    items.forEach(item => {
        item.name = item.name.toLowerCase();
        console.log('s: ' + search_text + ' i: ' + item.name)
        if(item.name.search(search_text) != -1) {
            result_items.push(item);
        }
    })
    return result_items;
}

function show_search_results(result_items) {
    let results_doc = document.getElementById('results');

    //  itrate through all result items and displayes it on page
    result_items.forEach(result_item => {
        var item_slip = document.createElement('DIV');
        item_slip.className = 'item-slip';

        var item_image = document.createElement('IMG');
        item_image.src = result_item.image;

        var item_info = document.createElement('DIV');
        item_info.className = 'info';
        item_info.innerHTML = "" +
            "<div>" + result_item.name + "</div>" +
            "<div>" + result_item.standard_selling_rate +  " Rs</div>";

        item_slip.append(item_image);
        item_slip.append(item_info);
        results_doc.append(item_slip);
    })


}