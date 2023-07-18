import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CRUD import Base, Organization, create_organization, retrieve_all_organizations, update_organization_data, \
    get_organization


class TestCRUD(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.SessionLocal = sessionmaker(bind=engine)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_create_organization(self):
        organization_data = {
            'name': 'Empresa de Teste',
            'resume': 'Empresa para fins de teste',
            'url': 'http://empresa-teste.com',
            'address': 'Rua dos Testes, 123',
            'contacts': ['contato1@empresa-teste.com', 'contato2@empresa-teste.com']
        }
        new_organization = create_organization(self.db, organization_data)
        self.assertEqual(new_organization.name, 'Empresa de Teste')

    def test_retrieve_all_organizations(self):
        organization_data = {
            "name": "Empresa de Teste",
            "resume": "Empresa para fins de teste",
            "url": "http://empresa-teste.com",
            "address": "Rua dos Testes, 123",
            "contacts": ["contato1@empresa-teste.com", "contato2@empresa-teste.com"]
        }
        create_organization(self.db, organization_data)
        organizations = retrieve_all_organizations(self.db)

        self.assertIsNotNone(organizations)
        self.assertEqual(len(organizations), 1)
        self.assertEqual(organizations[0].name, "Empresa de Teste")
        self.assertEqual(organizations[0].resume, "Empresa para fins de teste")
        self.assertEqual(organizations[0].url, "http://empresa-teste.com")
        self.assertEqual(organizations[0].address, "Rua dos Testes, 123")
        self.assertListEqual(organizations[0].contacts, ["contato1@empresa-teste.com", "contato2@empresa-teste.com"])

    def test_get_organization(self):
        organization_data = {
            'name': 'Empresa de Teste',
            'resume': 'Empresa para fins de teste',
            'url': 'http://empresa-teste.com',
            'address': 'Rua dos Testes, 123',
            'contacts': ['contato1@empresa-teste.com', 'contato2@empresa-teste.com']
        }
        new_organization = create_organization(self.db, organization_data)
        organization = get_organization(self.db, new_organization.id)
        self.assertEqual(organization, new_organization)

    def test_update_organization_data(self):
        organization_data = {
            "name": "Empresa de Teste",
            "resume": "Empresa para fins de teste",
            "url": "http://empresa-teste.com",
            "address": "Rua dos Testes, 123",
            "contacts": ["contato1@empresa-teste.com", "contato2@empresa-teste.com"]
        }
        create_organization(self.db, organization_data)

        updated_data = {
            "name": "Empresa Atualizada",
            "resume": "Empresa atualizada para fins de teste",
            "url": "http://empresa-atualizada.com",
            "address": "Rua das Atualizações, 456",
            "contacts": ["contato3@empresa-atualizada.com"]
        }

        updated_organization = update_organization_data(self.db, Organization(**updated_data, id=1))

        self.assertIsNotNone(updated_organization)
        self.assertEqual(updated_organization.name, "Empresa Atualizada")
        self.assertEqual(updated_organization.resume, "Empresa atualizada para fins de teste")
        self.assertEqual(updated_organization.url, "http://empresa-atualizada.com")
        self.assertEqual(updated_organization.address, "Rua das Atualizações, 456")
        self.assertListEqual(updated_organization.contacts, ["contato3@empresa-atualizada.com"])

        db_organization = get_organization(self.db, updated_organization.id)
        self.assertIsNotNone(db_organization)
        self.assertEqual(db_organization.name, "Empresa Atualizada")
        self.assertEqual(db_organization.resume, "Empresa atualizada para fins de teste")
        self.assertEqual(db_organization.url, "http://empresa-atualizada.com")
        self.assertEqual(db_organization.address, "Rua das Atualizações, 456")
        self.assertListEqual(db_organization.contacts, ["contato3@empresa-atualizada.com"])


if __name__ == '__main__':
    unittest.main()

#  python -m unittest test_CRUD.py
