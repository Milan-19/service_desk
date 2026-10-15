# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class RepairJob(Document):
	def validate(self):
		self.validate_dates()
		self.apply_default_labour_rate()
		self.calculate_totals()

	def validate_dates(self):
		if self.expected_delivery and getdate(self.expected_delivery) < getdate(self.received_on):
			frappe.throw(_("Expected Delivery cannot be before Received On date."))

	def apply_default_labour_rate(self):
		default_rate = frappe.db.get_single_value("Service Settings", "default_labour_rate")
		for row in self.labour_charges:
			if not row.rate:
				row.rate = flt(default_rate)


	def calculate_totals(self):
		for row in self.parts:
			row.amount = flt(row.qty) * flt(row.rate)
		for row in self.labour_charges:
			row.amount = flt(row.hours) * flt(row.rate)
		self.total_parts = sum(r.amount for r in self.parts)
		self.total_labour = sum(r.amount for r in self.labour_charges)
		self.grand_total = self.total_parts + self.total_labour

	def before_submit(self):
		if not self.technician:
			frappe.throw(_("Assign a technician before submitting."))