from unittest.mock import patch

from fastapi.testclient import TestClient

from Models.Organization import Organization
from main import app


class TestMainApp:
    def setup_method(self):
        self.client = TestClient(app)

    def teardown_method(self):
        pass

    @patch('main.retrieve_all_organizations')
    def test_get_all_organization(self, mock_retrieve_all_organizations):
        # criando uma lista de organizações de exemplo
        organizations = [
            Organization(id=1, name="Organization 1"),
            Organization(id=2, name="Organization 2"),
        ]

        mock_retrieve_all_organizations.return_value = organizations

        # solicitação GET para a rota '/api/v1/organizations'
        response = self.client.get("/api/v1/organizations")

        # verificando se o código de status da resposta é 200 (OK)
        assert response.status_code == 200

        # verificando se o corpo da resposta contém as organizações esperadas
        assert response.json() == [
            {"id": 1, "name": "Organization 1"},
            {"id": 2, "name": "Organization 2"},
        ]
