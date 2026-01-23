from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from types import SimpleNamespace

from tests.conftest import mock_session


def test_create_employer_success(client: TestClient, mock_session):

    sector = SimpleNamespace(name="TESTE")

    query_mock = mock_session.query.return_value
    filter_mock = query_mock.filter.return_value

    filter_mock.first.side_effect = [
    None,    # check employer
    sector   # get sector
]

    payload = {
        "name": "teste", 
        "sector_name": "teste",
        "password": "123",
        "emp_id": "9290",
        }
    
    response = client.post("/Employers/create_employer", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Employer created successfuly"