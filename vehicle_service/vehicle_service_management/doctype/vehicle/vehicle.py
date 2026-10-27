# Copyright (c) 2026, Anitta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Vehicle(Document):
    def validate(self):
        self.validate_registration_number()

    def validate_registration_number(self):
        if not self.registration_number:
            frappe.throw("Registration Number is required.")

        # Normalize registration numbers to avoid case/space variations
        self.registration_number = self.registration_number.strip().upper()

        existing_vehicle = frappe.db.exists(
            "Vehicle",
            {
                "registration_number": self.registration_number,
                "name": ["!=", self.name or ""],
            },
        )

        if existing_vehicle:
            frappe.throw(
                f"Vehicle with registration number "
                f"{self.registration_number} already exists."
            )