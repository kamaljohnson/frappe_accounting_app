import frappe

def get_context(context):
    context.company_name = frappe.get_all('Company')[0]['name']
    context.items = frappe.get_all('Item', fields=['image', 'name', 'standard_selling_rate'])
    return context