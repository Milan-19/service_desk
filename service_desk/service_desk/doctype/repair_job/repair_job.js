// Copyright (c) 2026, dev and contributors
// For license information, please see license.txt

frappe.ui.form.on("Repair Job", {
	setup(frm) {
		frm.set_query("technician", () => {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
	},

	refresh(frm) {
		if (!frm.is_new() && frm.doc.docstatus < 2) {
			frm.add_custom_button(__("Update Status"), () => {
				frappe.prompt(
					{
						fieldname: "status",
						label: __("Status"),
						fieldtype: "Select",
						options: "Received\nDiagnosed\nIn Repair\nReady\nDelivered",
						reqd: 1,
						default: frm.doc.status,
					},
					(values) => {
						frm.call("update_status", { status: values.status }).then(() => {
							frm.reload_doc();
						});
					},
					__("Update Status"),
				);
			});
		}
	},

	technician(frm) {
		if (!frm.doc.technician) return;
		frappe.call({
			method: "service_desk.service_desk.doctype.repair_job.repair_job.get_technician_workload",
			args: { technician: frm.doc.technician },
			callback: (r) => {
				frappe.show_alert({
					message: __("{0} has {1} open job(s)", [frm.doc.technician, r.message]),
					indicator: "blue",
				});
			},
		});
	},
});

frappe.ui.form.on("Repair Part", {
	qty: update_part_row,
	rate: update_part_row,
	parts_remove: calculate_totals,
});

frappe.ui.form.on("Repair Labour", {
	hours: update_labour_row,
	rate: update_labour_row,
	labour_charges_remove: calculate_totals,
});

function update_part_row(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate));
	calculate_totals(frm);
}

function update_labour_row(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", flt(row.hours) * flt(row.rate));
	calculate_totals(frm);
}

function calculate_totals(frm) {
	const total_parts = (frm.doc.parts || []).reduce((sum, r) => sum + flt(r.amount), 0);
	const total_labour = (frm.doc.labour_charges || []).reduce((sum, r) => sum + flt(r.amount), 0);
	frm.set_value({
		total_parts,
		total_labour,
		grand_total: total_parts + total_labour,
	});
}
