frappe.listview_settings["Repair Job"] = {
	get_indicator(doc) {
		const colors = {
			Received: "gray",
			Diagnosed: "orange",
			"In Repair": "blue",
			Ready: "green",
			Delivered: "darkgrey",
		};
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
};
