# Copyright (c) 2026, dev and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Count, Sum
from frappe.utils import add_days, flt


def execute(filters=None):
    filters = frappe._dict(filters or {})
    data = get_data(filters)
    return get_columns(), data, None, get_chart(data)


def get_columns():
    return [
        {"label": _("Technician"), "fieldname": "technician", "fieldtype": "Link", "options": "Technician", "width": 160},
        {"label": _("Jobs"), "fieldname": "jobs", "fieldtype": "Int", "width": 80},
        {"label": _("Delivered"), "fieldname": "delivered", "fieldtype": "Int", "width": 100},
        {"label": _("Parts"), "fieldname": "total_parts", "fieldtype": "Currency", "width": 120},
        {"label": _("Labour"), "fieldname": "total_labour", "fieldtype": "Currency", "width": 120},
        {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    job = frappe.qb.DocType("Repair Job")

    def base_query(*fields):
        query = frappe.qb.from_(job).select(job.technician, *fields).where(job.docstatus < 2)
        if filters.get("from_date"):
            query = query.where(job.received_on >= filters.from_date)
        if filters.get("to_date"):
            query = query.where(job.received_on < add_days(filters.to_date, 1))
        if filters.get("technician"):
            query = query.where(job.technician == filters.technician)
        return query.groupby(job.technician)

    rows = base_query(
        Count(job.name).as_("jobs"),
        Sum(job.total_parts).as_("total_parts"),
        Sum(job.total_labour).as_("total_labour"),
        Sum(job.grand_total).as_("grand_total"),
    ).run(as_dict=True)

    delivered = base_query(Count(job.name).as_("delivered")).where(
        job.workflow_state == "Delivered"
    ).run(as_dict=True)
    delivered_by_technician = {d.technician: d.delivered for d in delivered}

    for row in rows:
        row.delivered = delivered_by_technician.get(row.technician, 0)
        row.total_parts = flt(row.total_parts)
        row.total_labour = flt(row.total_labour)
        row.grand_total = flt(row.grand_total)
    return rows


def get_chart(data):
    if not data:
        return None
    return {
        "type": "bar",
        "data": {
            "labels": [row.technician or _("Unassigned") for row in data],
            "datasets": [{"name": _("Grand Total"), "values": [row.grand_total for row in data]}],
        },
    }