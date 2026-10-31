# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate

# STATUSES = ("Received", "Diagnosed", "In Repair", "Ready", "Delivered")

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

	@frappe.whitelist()
	def issue_parts(self):
		self.check_permission("write")
		
		if self.docstatus != 0:
			frappe.throw(_("Parts can only be issued on a draft job"))
		if self.stock_entry:
			frappe.throw(_("Parts were already issued on {0}").format(self.stock_entry))
		if not self.parts:
			frappe.throw(_("Add at least one part first"))
			
		warehouse = frappe.db.get_single_value("Service Settings", "default_warehouse")
		if not warehouse:
			frappe.throw(_("Set a Default Warehouse in Service Settings"))
			
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Issue"
		stock_entry.purpose = "Material Issue"
		stock_entry.company = frappe.db.get_value("Warehouse", warehouse, "company")
		stock_entry.remarks = _("Parts issued for {0}").format(self.name)
		
		
		for row in self.parts:
			stock_entry.append("items", {
                "item_code": row.item_code,
                "qty": row.qty,
                "s_warehouse": warehouse,
            })
			
		stock_entry.insert(ignore_permissions=True)
		stock_entry.submit()
		
		self.db_set("stock_entry", stock_entry.name)
		return stock_entry.name

@frappe.whitelist()
def get_technician_workload(technician):
    frappe.has_permission("Repair Job", "read", throw=True)
    return frappe.db.count("Repair Job", {
        "technician": technician,
        "workflow_state": ["in", ["Received", "Diagnosed", "In Repair"]],
        "docstatus": ["<", 2],
    })