# Copyright (c) 2021, Kamal Johnson and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Item(WebsiteGenerator):
	pass

@frappe.whitelist(allow_guest=False)
def add_item_to_cart(item_code):
	print('adding item {} to cart'.format(item_code))