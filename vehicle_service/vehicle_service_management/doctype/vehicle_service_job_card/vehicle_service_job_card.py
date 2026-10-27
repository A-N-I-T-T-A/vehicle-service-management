# Copyright (c) 2026, Anitta and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class VehicleServiceJobCard(Document):
    def validate(self):
        self.validate_status_transition()
        self.validate_tasks_for_progress()
        self.validate_tasks_before_completion()
        self.calculate_estimated_cost()

    def validate_status_transition(self):
        previous = self.get_doc_before_save()

        if not previous or previous.status == self.status:
            return

        allowed_transitions = {
            "Pending": ["In Progress", "Cancelled"],
            "In Progress": ["Completed", "Cancelled"],
            "Completed": [],
            "Cancelled": [],
        }

        allowed = allowed_transitions.get(previous.status, [])

        if self.status not in allowed:
            frappe.throw(
                f"Cannot change Job Card status from "
                f"{previous.status} to {self.status}."
            )

    def calculate_estimated_cost(self):
        total = 0

        for task in self.get("service_tasks") or []:
            total += task.task_cost or 0

        self.estimated_cost = total

    def on_update(self):
        if not self.service_booking:
            return

        if self.status == "In Progress":
            frappe.db.set_value(
                "Service Booking",
                self.service_booking,
                "status",
                "In Progress",
            )

        elif self.status == "Completed":
            frappe.db.set_value(
                "Service Booking",
                self.service_booking,
                "status",
                "Completed",
            )

        elif self.status == "Cancelled":
            frappe.db.set_value(
                "Service Booking",
                self.service_booking,
                "status",
                "Cancelled",
            )
    
    
    def validate_tasks_for_progress(self):
        if self.status != "In Progress":
            return

        tasks = self.get("service_tasks") or []

        if not tasks:
            frappe.throw(
                "Add at least one service task before starting the Job Card."
            )

        in_progress_tasks = [
            task for task in tasks
            if task.status == "In Progress"
        ]

        if not in_progress_tasks:
            frappe.throw(
                "At least one Service Task must be In Progress "
                "before the Job Card can be marked In Progress."
            )


    def validate_tasks_before_completion(self):
        if self.status != "Completed":
            return

        tasks = self.get("service_tasks") or []

        if not tasks:
            frappe.throw(
                "Add at least one service task before completing the Job Card."
            )

        incomplete_tasks = [
            task.task_description or task.name
            for task in tasks
            if task.status != "Completed"
        ]

        if incomplete_tasks:
            frappe.throw(
                "Complete all service tasks before completing the Job Card: "
                + ", ".join(incomplete_tasks)
            )
