import frappe
from frappe import _
from frappe.model.document import Document


class RepairInvoiceExtension(Document):
    def validate(self):
        super().validate()
        self.validate_repair_job_customer()

    def validate_repair_job_customer(self):
        job = self.get("custom_repair_job")
        if not job:
            return
        job_customer = frappe.db.get_value("Repair Job", job, "customer")
        if job_customer != self.customer:
            frappe.throw(
                _("Customer must match the Repair Job's customer ({0})").format(job_customer)
            )