import frappe

def get_context(context):
    context.company_name = frappe.get_all('Company')[0]['name']
    context.result_items = frappe.get_all('Item', fields=['image', 'name', 'standard_selling_rate'])
    return context

@frappe.whitelist(allow_guest=True)
def search_text(text):
    print('{} searching...'.format(text))