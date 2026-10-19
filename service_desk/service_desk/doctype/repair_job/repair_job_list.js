// frappe.listview_settings["Repair Job"] = {
// 	get_indicator(doc) {
// 		const colors = {
// 			Received: "gray",
// 			Diagnosed: "orange",
// 			"In Repair": "blue",
// 			Ready: "green",
// 			Delivered: "darkgrey",
// 		};
// 		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
// 	},
// };

frappe.listview_settings["Repair Job"] = {
	has_indicator_for_draft: true,
	has_indicator_for_cancelled: true,

	get_indicator(doc) {
		// Edit this map to match the exact options in your Status Select field
		const colors = {
			Received: "blue",
			"In Repair": "orange",
			Completed: "green",
			Cancelled: "red",
		};
		const color = colors[doc.status] || "gray";
		// Third item is the filter applied when the badge is clicked
		return [__(doc.status), color, "status,=," + doc.status];
	},
};
