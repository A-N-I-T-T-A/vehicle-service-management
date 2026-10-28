# Copyright (c) 2026, Anitta and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Job Card",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Vehicle Service Job Card",
            "width": 180,
        },
        {
            "label": "Service Booking",
            "fieldname": "service_booking",
            "fieldtype": "Link",
            "options": "Service Booking",
            "width": 180,
        },
        {
            "label": "Technician",
            "fieldname": "assigned_technician",
            "fieldtype": "Link",
            "options": "User",
            "width": 200,
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Estimated Cost",
            "fieldname": "estimated_cost",
            "fieldtype": "Currency",
            "width": 140,
        },
    ]

    conditions = []
    values = {}

    user = frappe.session.user
    roles = frappe.get_roles(user)

    if user != "Administrator" and "Technician" in roles:
        conditions.append(
            "assigned_technician = %(current_user)s"
        )
        values["current_user"] = user

    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters["status"]

    if filters.get("assigned_technician"):
        conditions.append(
            "assigned_technician = %(assigned_technician)s"
        )
        values["assigned_technician"] = filters["assigned_technician"]

    if filters.get("from_date"):
        conditions.append("creation >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("creation < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)")
        values["to_date"] = filters["to_date"]

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )

    data = frappe.db.sql(
        f"""
        SELECT
            name,
            service_booking,
            assigned_technician,
            status,
            estimated_cost
        FROM `tabVehicle Service Job Card`
        {where_clause}
        ORDER BY modified DESC
        """,
        values,
        as_dict=True,
    )

    return columns, data

