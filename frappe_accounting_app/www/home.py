import frappe

def get_context(context):
    context.company_name = frappe.get_all('Company')[0]['name']
    context.result_items = frappe.get_all('Item', fields=['image', 'name', 'standard_selling_rate'])
    return context

def search(text):
    print('searching for {}'.format(text))