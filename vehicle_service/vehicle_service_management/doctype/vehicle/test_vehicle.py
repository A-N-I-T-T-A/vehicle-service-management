// Copyright (c) 2026, Anitta and contributors
// For license information, please see license.txt

import frappe
import uuid
from frappe.tests.utils import FrappeTestCase


class TestVehicle(FrappeTestCase):

    def unique_registration(self):
        return f"T{uuid.uuid4().hex[:10].upper()}"

    def test_registration_number_is_required(self):
        vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "registration_number": "",
        })

        with self.assertRaises(frappe.ValidationError):
            vehicle.insert(ignore_permissions=True)

    def test_duplicate_registration_number_is_rejected(self):
        registration_number = self.unique_registration()

        first_vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "registration_number": registration_number,
        })
        first_vehicle.insert(ignore_permissions=True)

        duplicate_vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "registration_number": registration_number,
        })

        with self.assertRaises(
            (frappe.ValidationError, frappe.DuplicateEntryError)
        ):
            duplicate_vehicle.insert(ignore_permissions=True)

    def test_registration_number_is_normalized(self):
        registration_number = self.unique_registration().lower()

        vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "registration_number": f"  {registration_number}  ",
        })

        vehicle.validate()

        self.assertEqual(
            vehicle.registration_number,
            registration_number.strip().upper(),
        )
