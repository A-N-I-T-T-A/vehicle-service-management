// Copyright (c) 2026, Anitta and contributors
// For license information, please see license.txt


frappe.ui.form.on("Service Booking", {
    setup(frm) {
        frm.set_query("vehicle", () => {
            if (!frm.doc.customer) {
                return {
                    filters: {
                        name: ["in", []]
                    }
                };
            }

            return {
                filters: {
                    customer: frm.doc.customer
                }
            };
        });
    },

    customer(frm) {
        if (frm.doc.vehicle) {
            frappe.db.get_value(
                "Vehicle",
                frm.doc.vehicle,
                "customer"
            ).then((r) => {
                if (
                    r.message &&
                    r.message.customer !== frm.doc.customer
                ) {
                    frm.set_value("vehicle", "");
                }
            });
        }
    }
});


frappe.ui.form.on("Service Booking", {
    refresh(frm) {
        if (
            frm.is_new() ||
            !frm.doc.name ||
            frm.doc.status === "Cancelled" ||
            frm.doc.status === "Completed"
        ) {
            return;
        }

        if (frappe.user.has_role("Service Advisor")) {
            frm.add_custom_button(
                __("Create Job Card"),
                () => {
                    frappe.new_doc(
                        "Vehicle Service Job Card",
                        {
                            service_booking: frm.doc.name
                        }
                    );
                }
            );
        }
    }
});
