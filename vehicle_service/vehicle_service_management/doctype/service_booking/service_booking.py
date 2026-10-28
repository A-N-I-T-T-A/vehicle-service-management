# Copyright (c) 2026, Anitta and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class ServiceBooking(Document):
    def validate(self):
        self.validate_vehicle_customer()
        self.validate_booking_date()
        self.validate_vehicle_availability()
        self.validate_status_transition()

    def validate_vehicle_customer(self):
        if not self.customer or not self.vehicle:
            return

        vehicle_customer = frappe.db.get_value(
            "Vehicle",
            self.vehicle,
            "customer",
        )

        if not vehicle_customer:
            frappe.throw("The selected vehicle does not have a customer.")

        if vehicle_customer != self.customer:
            frappe.throw(
                "The selected vehicle must belong to the selected customer."
            )

    def validate_booking_date(self):
        if self.booking_date and getdate(self.booking_date) < getdate(nowdate()):
            frappe.throw("Booking Date cannot be in the past.")

    def validate_vehicle_availability(self):
        if not self.vehicle or not self.booking_date:
            return

        active_statuses = ["Booked", "Confirmed", "In Progress"]

        filters = {
            "vehicle": self.vehicle,
            "booking_date": self.booking_date,
            "status": ["in", active_statuses],
        }

        if not self.is_new():
            filters["name"] = ["!=", self.name]

        existing_booking = frappe.db.exists("Service Booking", filters)

        if existing_booking:
            frappe.throw(
                "This vehicle already has an active booking on this date."
            )

    def validate_status_transition(self):
        previous = self.get_doc_before_save()

        if not previous or previous.status == self.status:
            return

        self.check_status_transition(previous.status, self.status)

    @staticmethod
    def check_status_transition(previous_status, new_status):
        allowed_transitions = {
            "Booked": ["Confirmed", "Cancelled"],
            "Confirmed": ["In Progress", "Cancelled"],
            "In Progress": ["Completed", "Cancelled"],
            "Completed": [],
            "Cancelled": [],
        }

        allowed = allowed_transitions.get(previous_status, [])

        if new_status not in allowed:
            frappe.throw(
                f"Cannot change booking status from "
                f"{previous_status} to {new_status}."
            )
