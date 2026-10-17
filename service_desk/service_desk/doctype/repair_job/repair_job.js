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

	// refresh(frm) {
	// 	console.log("Repair Job form refreshed:", frm.doc.name);
	// },
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
