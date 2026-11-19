# Copyright (c) 2026, dev and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


class IntegrationTestRepairJob(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		# Skip automatic test record generation if causing issues
		super(IntegrationTestCase, cls).setUpClass()

	def make_job(self):
		job = frappe.new_doc("Repair Job")
		job.received_on = "2026-11-01 10:00:00"
		job.append("parts", {"item_code": "Dummy", "qty": 2, "rate": 500})
		job.append("labour_charges", {"description": "Fit screen", "hours": 3, "rate": 200})
		return job

	def test_totals_are_calculated(self):
		job = self.make_job()
		job.calculate_totals()
		self.assertEqual(job.total_parts, 1000)
		self.assertEqual(job.total_labour, 600)
		self.assertEqual(job.grand_total, 1600)

	def test_delivery_cannot_be_before_received(self):
		job = self.make_job()
		job.expected_delivery = "2026-10-31"
		with self.assertRaises(frappe.ValidationError):
			job.validate_dates()
