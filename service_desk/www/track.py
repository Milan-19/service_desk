import frappe

no_cache = 1


def get_context(context):
    code = (frappe.form_dict.get("code") or "").strip()
    context.code = code
    context.found = None
    context.job_state = None

    if code:
        context.found = frappe.db.get_value(
            "Repair Request",
            {"tracking_code": code},
            ["name", "status", "repair_job", "creation"],
            as_dict=True,
        )
        if context.found and context.found.repair_job:
            context.job_state = frappe.db.get_value(
                "Repair Job", context.found.repair_job, "workflow_state"
            )
    return context