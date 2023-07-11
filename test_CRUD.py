import unittest
from unittest.mock import MagicMock

from CRUD import create_organization, create_employee, retrieve_all_organizations, get_organization, \
    update_organization_data, get_all_employees
from Models.Employee import Employee
from Models.Organization import Organization


class CRUDTests(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.organization = Organization(name="Test Organization")
        self.employee = Employee(name="John Doe", organization_id=1)

    def test_create_organization(self):
        created_organization = create_organization(self.db, self.organization)
        self.assertIsNotNone(created_organization)
        self.assertEqual(created_organization.name, "Test Organization")

    def test_create_employee(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.organization
        created_employee = create_employee(self.db, self.employee)
        self.assertIsNotNone(created_employee)
        self.assertEqual(created_employee.name, "John Doe")
        self.assertEqual(created_employee.organization_id, 1)

    def test_retrieve_all_organizations(self):
        self.db.query.return_value.all.return_value = [self.organization]
        organizations = retrieve_all_organizations(self.db)
        self.assertIsNotNone(organizations)
        self.assertEqual(len(organizations), 1)
        self.assertEqual(organizations[0].name, "Test Organization")

    def test_get_organization(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.organization
        retrieved_organization = get_organization(self.db, 1)
        self.assertIsNotNone(retrieved_organization)
        self.assertEqual(retrieved_organization.name, "Test Organization")

    def test_update_organization_data(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.organization
        updated_organization = update_organization_data(self.db, self.organization)
        self.assertIsNotNone(updated_organization)
        self.assertEqual(updated_organization.name, "Test Organization")

    def test_get_all_employees(self):
        self.db.query.return_value.all.return_value = [self.employee]
        employees = get_all_employees(self.db)
        self.assertIsNotNone(employees)
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].name, "John Doe")
        self.assertEqual(employees[0].organization_id, 1)


if __name__ == '__main__':
    unittest.main()
