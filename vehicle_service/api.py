// Copyright (c) 2026, Anitta and contributors
// For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate


def require_role(allowed_roles):
    user = frappe.session.user

    if user == "Administrator":
        return

    user_roles = frappe.get_roles(user)

    if not any(role in user_roles for role in allowed_roles):
        frappe.throw(
            "You do not have permission to perform this action.",
            frappe.PermissionError,
        )


@frappe.whitelist(methods=["POST"])
def create_service_booking(customer, vehicle, booking_date, service_type):
    require_role(["Service Advisor"])

    if not frappe.has_permission("Service Booking", "create"):
        frappe.throw(
            "Not permitted to create Service Bookings.",
            frappe.PermissionError,
        )

    if not all([customer, vehicle, booking_date, service_type]):
        frappe.throw(
            "Customer, vehicle, booking date, and service type are required."
        )

    if not frappe.db.exists("Customer", customer):
        frappe.throw("Customer does not exist.")

    if not frappe.db.exists("Vehicle", vehicle):
        frappe.throw("Vehicle does not exist.")

    valid_service_types = [
        "General Service",
        "Oil Change",
        "Repair",
        "Inspection",
    ]

    if service_type not in valid_service_types:
        frappe.throw("Invalid service type.")

    try:
        booking_date = getdate(booking_date)
    except (TypeError, ValueError):
        frappe.throw("Invalid booking date.")

    if booking_date < getdate(nowdate()):
        frappe.throw("Booking Date cannot be in the past.")

    vehicle_customer = frappe.db.get_value(
        "Vehicle", vehicle, "customer"
    )

    if vehicle_customer != customer:
        frappe.throw(
            "The selected vehicle must belong to the selected customer."
        )

    doc = frappe.get_doc({
        "doctype": "Service Booking",
        "customer": customer,
        "vehicle": vehicle,
        "booking_date": booking_date,
        "service_type": service_type,
        "status": "Booked",
    })

    doc.insert()

    return {
        "name": doc.name,
        "status": doc.status,
    }


@frappe.whitelist(methods=["GET"])
def get_service_booking(name):
    if not name:
        frappe.throw("Booking name is required.")

    if not frappe.db.exists("Service Booking", name):
        frappe.throw(
            "Service Booking not found.",
            frappe.DoesNotExistError,
        )

    require_role(["Service Advisor", "Technician"])

    if not frappe.has_permission("Service Booking", "read", name):
        frappe.throw(
            "Not permitted to read this booking.",
            frappe.PermissionError,
        )

    doc = frappe.get_doc("Service Booking", name)

    return {
        "name": doc.name,
        "customer": doc.customer,
        "vehicle": doc.vehicle,
        "booking_date": str(doc.booking_date),
        "service_type": doc.service_type,
        "status": doc.status,
    }


@frappe.whitelist(methods=["POST"])
def update_booking_status(name, status):
    require_role(["Service Advisor"])

    if not name or not status:
        frappe.throw("Booking name and status are required.")

    if not frappe.db.exists("Service Booking", name):
        frappe.throw(
            "Service Booking not found.",
            frappe.DoesNotExistError,
        )

    if not frappe.has_permission("Service Booking", "write", name):
        frappe.throw(
            "Not permitted to update this booking.",
            frappe.PermissionError,
        )

    allowed_statuses = [
        "Booked",
        "Confirmed",
        "In Progress",
        "Completed",
        "Cancelled",
    ]

    if status not in allowed_statuses:
        frappe.throw("Invalid booking status.")

    doc = frappe.get_doc("Service Booking", name)
    doc.status = status

    # The Service Booking controller validates status transitions.
    doc.save()

    return {
        "name": doc.name,
        "status": doc.status,
    }


def job_card_has_permission(
    doc, user=None, permission_type=None, ptype=None
):
    user = user or frappe.session.user
    permission_type = permission_type or ptype

    if user == "Administrator":
        return None

    roles = frappe.get_roles(user)

    if "Service Advisor" in roles:
        return None

    if "Technician" in roles:
        if permission_type in ("read", "write"):
            if doc.get("assigned_technician") != user:
                return False

        return None

    return None


def job_card_query(user=None):
    user = user or frappe.session.user

    if user == "Administrator":
        return None

    roles = frappe.get_roles(user)

    if "Service Advisor" in roles:
        return None

    if "Technician" in roles:
        return (
            "`tabVehicle Service Job Card`.`assigned_technician` = "
            + frappe.db.escape(user)
        )

    return None
