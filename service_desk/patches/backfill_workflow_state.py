import frappe


def execute():
	job = frappe.qb.DocType("Repair Job")
	for docstatus, state in ((0, "Received"), (1, "Delivered")):
		(
			frappe.qb.update(job)
			.set(job.workflow_state, state)
			.where(job.docstatus == docstatus)
			.where((job.workflow_state.isnull()) | (job.workflow_state == ""))
			.run()
		)
