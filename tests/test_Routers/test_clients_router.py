import pytest
from fastapi.testclient import TestClient
from types import SimpleNamespace
from unittest.mock import MagicMock

from main import app
from app.core.Dependecies import Init_Session

class ClientsTestsRouter:

    def setup_method(self):
        self.mock_session = MagicMock()
        def override_db():
            return self.mock_session
        app.dependency_overrides[Init_Session] = override_db
        self.client = TestClient(app)
        self.client_db = [
            {
                "name": "TESTE",
                "contact": "TESTE",
                "email": "teste@gmail.com",
                "phone": "14932948",
            },
            {
                "name": "TESTE2",
                "contact": "TESTE2",
                "email": "teste2@gmail.com",
                "phone": "149329428",
            },
        ]

    def teardown_method(self):
        app.dependency_overrides = {}

    def test_create_clients_success(self):
    # Arrange
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        self.mock_session.add.return_value = None
        self.mock_session.commit.return_value = None

        payload = self.client_db[0]

        # Act
        response = self.client.post("/Clients/create_client", json=payload)

        # Assert
        assert response.status_code == 200

        body = response.json()

        assert body["message"] == "Client created successfuly"
        assert body["Client"] == "TESTE"

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()



   

