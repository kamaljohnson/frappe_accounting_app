import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Log in to access this page."), frappe.PermissionError)

    customer = get_session_customer(frappe.session.user)

    context.company_name = frappe.get_all('Company')[0]['name']
    context.items = frappe.get_all('Item', fields=['image', 'name', 'standard_selling_rate'])
    return context

@frappe.whitelist(allow_guest=False)
def get_session_customer(user_name):
    """
    If a customer object is present for the given user returns the same,
    else creates one and returns it.

    Usage: get_session_customer(user) | use 'frappe.session.user' to get current user
    """

    user = frappe.get_doc('User', user_name)

    customers = frappe.get_all('Customer', filters={'user': ['=', user.name]})

    if len(customers) == 0:
        # If not a customer, creating a new customer for user.
        customer = frappe.get_doc({
            'doctype': 'Customer',
            'full_name': user.name,
            'user': user.name,
        })
        customer.insert()
        frappe.db.commit()
    else:
        # using the exsisting customer for the given user
        customer = customers[0]

    return customer