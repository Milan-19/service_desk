import frappe
from frappe.tests import IntegrationTestCase

from service_desk.permissions import get_repair_job_conditions, is_technician_only


class IntegrationTestPermissions(IntegrationTestCase):
    def test_administrator_has_no_extra_filter(self):
        self.assertEqual(get_repair_job_conditions("Administrator"), "")

    def test_technician_sees_only_own_jobs(self):
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "test.tech@example.com",
                "first_name": "Test",
                "send_welcome_email": 0,
                "roles": [{"role": "Service Technician"}],
            }
        ).insert(ignore_permissions=True)
        frappe.get_doc(
            {"doctype": "Technician", "full_name": "Test Tech", "user": user.name, "enabled": 1}
        ).insert(ignore_permissions=True)

        self.assertTrue(is_technician_only(user.name))
        self.assertIn("Test Tech", get_repair_job_conditions(user.name))