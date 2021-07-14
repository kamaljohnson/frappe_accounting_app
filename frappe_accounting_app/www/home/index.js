// TODO: add on searchbar input text change trigger search
frappe.ready(function(){
    $('#test_button').on('click', function(){
        console.log('Here');
        frappe.call({
            method: "accounting_app.www.home.search_text",
            args: {
                "text": 'input text',
            }
        })
    });
})