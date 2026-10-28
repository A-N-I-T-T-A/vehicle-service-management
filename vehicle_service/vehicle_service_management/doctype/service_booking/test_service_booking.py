# Copyright (c) 2026, Anitta and Contributors
# See license.txt


import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today

from vehicle_service.vehicle_service_management.doctype.service_booking.service_booking import (
    ServiceBooking,
)


class TestServiceBooking(FrappeTestCase):

    def test_valid_status_transition(self):
        valid_transitions = [
            ("Booked", "Confirmed"),
            ("Booked", "Cancelled"),
            ("Confirmed", "In Progress"),
            ("Confirmed", "Cancelled"),
            ("In Progress", "Completed"),
            ("In Progress", "Cancelled"),
        ]

        for old_status, new_status in valid_transitions:
            with self.subTest(old_status=old_status, new_status=new_status):
                ServiceBooking.check_status_transition(
                    old_status, new_status
                )

    def test_invalid_status_transition(self):
        invalid_transitions = [
            ("Booked", "Completed"),
            ("Confirmed", "Booked"),
            ("Completed", "Cancelled"),
            ("Cancelled", "Confirmed"),
        ]

        for old_status, new_status in invalid_transitions:
            with self.subTest(old_status=old_status, new_status=new_status):
                with self.assertRaises(frappe.ValidationError):
                    ServiceBooking.check_status_transition(
                        old_status, new_status
                    )

    def test_past_booking_date_is_rejected(self):
        # Supply valid existing Customer and Vehicle records.
        customer = frappe.db.get_value("Customer", {}, "name")
        vehicle = frappe.db.get_value("Vehicle", {}, "name")

        if not customer or not vehicle:
            self.skipTest(
                "Create a test Customer and Vehicle before running this test."
            )

        booking = frappe.get_doc({
            "doctype": "Service Booking",
            "customer": customer,
            "vehicle": vehicle,
            "booking_date": add_days(today(), -1),
            "service_type": "General Service",
        })

        with self.assertRaises(frappe.ValidationError):
            booking.insert(ignore_permissions=True)

    def test_vehicle_customer_mismatch_is_rejected(self):
        customers = frappe.get_all("Customer", pluck="name", limit=2)
        vehicles = frappe.get_all(
            "Vehicle",
            fields=["name", "customer"],
            limit=20,
        )

        if len(customers) < 2:
            self.skipTest("At least two Customer records are needed.")

        vehicle = next(
            (v for v in vehicles if v.customer and v.customer != customers[0]),
            None,
        )

        if not vehicle:
            self.skipTest(
                "A Vehicle linked to a different Customer is required."
            )

        booking = frappe.get_doc({
            "doctype": "Service Booking",
            "customer": customers[0],
            "vehicle": vehicle.name,
            "booking_date": add_days(today(), 5),
            "service_type": "General Service",
        })

        with self.assertRaises(frappe.ValidationError):
            booking.insert(ignore_permissions=True)

