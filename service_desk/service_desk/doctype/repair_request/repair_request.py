# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RepairRequest(Document):
	def before_insert(self):
		self.tracking_code = frappe.generate_hash(length=10)
