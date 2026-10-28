// Copyright (c) 2026, Anitta and contributors
// For license information, please see license.txt


frappe.query_reports["Vehicle Service Job Card Report"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nPending\nIn Progress\nCompleted\nCancelled"
        },
        {
			fieldname: "assigned_technician",
			label: __("Technician"),
			fieldtype: "Link",
			options: "User",
			default: frappe.session.user,
			read_only: frappe.user.has_role("Technician")
		},
        {
            fieldname: "from_date",
            label: __("Created From"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("Created To"),
            fieldtype: "Date"
        }
    ]
};

