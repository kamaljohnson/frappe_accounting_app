import frappe

def get_context(context):
    context.company_name = frappe.get_all('Company')[0]['name']
    return context