import unittest
from unittest.mock import Mock

from sqlalchemy.orm import Session

from Models.Employee import Employee
from Models.Organization import Organization
from camada_de_negocio import retrieve_all_organizations, get_all_employees


class TestCamadaDeNegocio(unittest.TestCase):
    def setUp(self):
        self.db = Mock(spec=Session)

    def tearDown(self):
        pass

    def test_retrieve_all_organizations(self):
        organizations = []
        self.db.query.return_value.all.return_value = organizations

        result = retrieve_all_organizations(self.db)

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_get_all_employees(self):
        organizations = [
            Organization(id=1, name="Org1"),
            Organization(id=2, name="Org2"),
            Organization(id=3, name="Org3"),
        ]
        employees = [
            Employee(id=1, name="Employee1", organization_id=1),
            Employee(id=2, name="Employee2", organization_id=2),
            Employee(id=3, name="Employee3", organization_id=3),
        ]
        self.db.query.return_value.all.side_effect = [organizations, employees]

        result = get_all_employees(self.db)

        self.assertEqual(len(result), len(employees))
        self.assertEqual(result, employees)


if __name__ == '__main__':
    unittest.main()
