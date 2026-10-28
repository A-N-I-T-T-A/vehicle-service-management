# Copyright (c) 2026, Anitta and Contributors
# See license.txt


import frappe
from unittest.mock import patch
from frappe.tests.utils import FrappeTestCase

from vehicle_service.vehicle_service_management.doctype.vehicle_service_job_card.vehicle_service_job_card import (
    VehicleServiceJobCard,
)


class TestVehicleServiceJobCard(FrappeTestCase):

    def make_job_card(self, status="Pending", tasks=None):
        return frappe.get_doc({
            "doctype": "Vehicle Service Job Card",
            "status": status,
            "service_tasks": tasks or [],
        })

    def test_valid_status_transition(self):
        valid_transitions = [
            ("Pending", "In Progress"),
            ("Pending", "Cancelled"),
            ("In Progress", "Completed"),
            ("In Progress", "Cancelled"),
        ]

        for old_status, new_status in valid_transitions:
            with self.subTest(old_status=old_status, new_status=new_status):
                job_card = self.make_job_card(status=new_status)
                previous = frappe._dict(status=old_status)

                with patch.object(
                    job_card, "get_doc_before_save", return_value=previous
                ):
                    job_card.validate_status_transition()

    def test_invalid_status_transition(self):
        invalid_transitions = [
            ("Pending", "Completed"),
            ("In Progress", "Pending"),
            ("Completed", "Cancelled"),
            ("Cancelled", "In Progress"),
        ]

        for old_status, new_status in invalid_transitions:
            with self.subTest(old_status=old_status, new_status=new_status):
                job_card = self.make_job_card(status=new_status)
                previous = frappe._dict(status=old_status)

                with patch.object(
                    job_card, "get_doc_before_save", return_value=previous
                ):
                    with self.assertRaises(frappe.ValidationError):
                        job_card.validate_status_transition()

    def test_estimated_cost_calculation(self):
        job_card = self.make_job_card(tasks=[
            {
                "task_description": "Oil change",
                "estimated_hours": 1,
                "task_cost": 500,
                "status": "Pending",
            },
            {
                "task_description": "Inspection",
                "estimated_hours": 2,
                "task_cost": 750,
                "status": "Pending",
            },
        ])

        job_card.calculate_estimated_cost()

        self.assertEqual(job_card.estimated_cost, 1250)

    def test_job_card_cannot_start_without_tasks(self):
        job_card = self.make_job_card(status="In Progress")

        with self.assertRaises(frappe.ValidationError):
            job_card.validate_tasks_for_progress()

    def test_job_card_requires_in_progress_task(self):
        job_card = self.make_job_card(
            status="In Progress",
            tasks=[
                {
                    "task_description": "Oil change",
                    "task_cost": 500,
                    "status": "Pending",
                }
            ],
        )

        with self.assertRaises(frappe.ValidationError):
            job_card.validate_tasks_for_progress()

    def test_job_card_can_start_with_in_progress_task(self):
        job_card = self.make_job_card(
            status="In Progress",
            tasks=[
                {
                    "task_description": "Oil change",
                    "task_cost": 500,
                    "status": "In Progress",
                }
            ],
        )

        job_card.validate_tasks_for_progress()

    def test_job_card_cannot_complete_without_tasks(self):
        job_card = self.make_job_card(status="Completed")

        with self.assertRaises(frappe.ValidationError):
            job_card.validate_tasks_before_completion()

    def test_job_card_cannot_complete_with_incomplete_tasks(self):
        job_card = self.make_job_card(
            status="Completed",
            tasks=[
                {
                    "task_description": "Oil change",
                    "task_cost": 500,
                    "status": "In Progress",
                }
            ],
        )

        with self.assertRaises(frappe.ValidationError):
            job_card.validate_tasks_before_completion()

    def test_job_card_can_complete_when_all_tasks_are_completed(self):
        job_card = self.make_job_card(
            status="Completed",
            tasks=[
                {
                    "task_description": "Oil change",
                    "task_cost": 500,
                    "status": "Completed",
                },
                {
                    "task_description": "Inspection",
                    "task_cost": 750,
                    "status": "Completed",
                },
            ],
        )

        job_card.validate_tasks_before_completion()
