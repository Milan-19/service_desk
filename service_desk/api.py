import frappe


@frappe.whitelist(methods=["GET"])
def get_job_status(job):
    doc = frappe.get_doc("Repair Job", job)
    doc.check_permission("read")
    return {
        "job": doc.name,
        "customer": doc.customer_name,
        "state": doc.workflow_state,
        "expected_delivery": doc.expected_delivery,
    }