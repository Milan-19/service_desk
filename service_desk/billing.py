import frappe


def link_invoice_to_repair_job(doc, method=None):
    job = doc.get("custom_repair_job")
    if not job:
        return
    frappe.db.set_value(
        "Repair Job",
        job,
        {"sales_invoice": doc.name, "billed_amount": doc.grand_total},
    )


def unlink_invoice_from_repair_job(doc, method=None):
    job = doc.get("custom_repair_job")
    if not job:
        return
    frappe.db.set_value(
        "Repair Job",
        job,
        {"sales_invoice": None, "billed_amount": 0},
    )