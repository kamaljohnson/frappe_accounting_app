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

       console.log('serach input: ' + document.getElementById('search_input').value)
       frappe.call({
            method: 'frappe_accounting_app.www.home.index.search_text',
            args: {
                "text": document.getElementById('search_input').value,
            }
       })
     }
   });
 });