# Copyright (c) 2026, Anitta and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Booking ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Service Booking",
            "width": 180,
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180,
        },
        {
            "label": "Vehicle",
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "options": "Vehicle",
            "width": 150,
        },
        {
            "label": "Booking Date",
            "fieldname": "booking_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Service Type",
            "fieldname": "service_type",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120,
        },
    ]

    conditions = []
    values = {}

    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters["status"]

    if filters.get("customer"):
        conditions.append("customer = %(customer)s")
        values["customer"] = filters["customer"]

    if filters.get("from_date"):
        conditions.append("booking_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("booking_date <= %(to_date)s")
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
            customer,
            vehicle,
            booking_date,
            service_type,
            status
        FROM `tabService Booking`
        {where_clause}
        ORDER BY booking_date DESC
        """,
        values,
        as_dict=True,
    )

    return columns, data
