import frappe

FULL_ACCESS_ROLES = {"System Manager", "Service Manager", "Service Front Desk"}


def is_technician_only(user):
    roles = set(frappe.get_roles(user))
    return "Service Technician" in roles and not (roles & FULL_ACCESS_ROLES)


def get_technician_of(user):
    return frappe.db.get_value("Technician", {"user": user}, "name")


def get_repair_job_conditions(user=None):
    user = user or frappe.session.user
    if not is_technician_only(user):
        return ""
    technician = get_technician_of(user)
    if not technician:
        return "1=0"
    return f"`tabRepair Job`.technician = {frappe.db.escape(technician)}"


def has_repair_job_permission(doc, ptype=None, user=None, debug=False):
    user = user or frappe.session.user
    if not is_technician_only(user):
        return None
    if doc.technician and doc.technician == get_technician_of(user):
        return None
    return False