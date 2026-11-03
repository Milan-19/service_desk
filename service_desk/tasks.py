import frappe
from frappe import _
from frappe.utils import today
from frappe.utils.user import get_users_with_role

OPEN_STATES = ["Received", "Diagnosed", "In Repair", "Ready"]


def mark_overdue_jobs():
    overdue_jobs = frappe.get_all(
        "Repair Job",
        filters={
            "expected_delivery": ["<", today()],
            "workflow_state": ["in", OPEN_STATES],
            "docstatus": 0,
        },
        pluck="name",
    )
    for job_name in overdue_jobs:
        frappe.enqueue(
            "service_desk.tasks.notify_overdue_job",
            queue="short",
            repair_job=job_name,
        )


def notify_overdue_job(repair_job):
    for manager in get_users_with_role("Service Manager"):
        already_open = frappe.db.exists(
            "ToDo",
            {
                "reference_type": "Repair Job",
                "reference_name": repair_job,
                "allocated_to": manager,
                "status": "Open",
            },
        )
        if already_open:
            continue
        frappe.get_doc(
            {
                "doctype": "ToDo",
                "allocated_to": manager,
                "reference_type": "Repair Job",
                "reference_name": repair_job,
                "description": _("Repair job {0} is overdue").format(repair_job),
            }
        ).insert(ignore_permissions=True)