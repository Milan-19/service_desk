frappe.ui.form.on("Sales Invoice", {
	refresh(frm) {
		if (frm.doc.custom_repair_job) {
			frm.add_custom_button(__("Repair Job"), () => {
				frappe.set_route("Form", "Repair Job", frm.doc.custom_repair_job);
			});
		}
	},
});
