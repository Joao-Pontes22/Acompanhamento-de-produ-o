from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from types import SimpleNamespace

from tests.conftest import mock_session



def test_create_component_success(client: TestClient,
                                   mock_session
                                   ):

    mock_session.query.return_value.filter.return_value.first.return_value = None

    supplier = SimpleNamespace(name="TESTE")

    mock_session.query.return_value.filter.return_value.first.side_effect = None, supplier 

    payload = {
        "part_number" : "teste",
        "description" : "teste",
        "supplier_name" : "teste",
        "cost" : 200,
        "component_type": "RAW",
        }

    response = client.post("/Components/create_component", json=payload)

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Component created successful"
    assert body["Component"] == "TESTE"

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_all_component_success(client: TestClient,
                                   mock_session):
    
    component_db = [{
        "id": 1,
        "part_number" : "teste",
        "description" : "teste",
        "supplier_name" : "teste",
        "cost" : 200,
        "component_type": "RAW",
        },
        {
        "id": 2,
        "part_number" : "teste2",
        "description" : "teste2",
        "supplier_name" : "teste2",
        "cost" : 200,
        "component_type": "RAW",
        }]

    mock_session.query.return_value.filter.return_value.all.return_value = component_db

    response = client.get("/Components/get_all_components")

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body[0]["part_number"] == "teste"
    assert body[1]["part_number"] == "teste2"


def test_get_component_filtred_success(client: TestClient,
                                   mock_session):
    
    component_db = [{
        "id": 1,
        "part_number" : "teste",
        "description" : "teste",
        "supplier_name" : "teste",
        "cost" : 200,
        "component_type": "RAW",
        },
        {
        "id": 2,
        "part_number" : "teste2",
        "description" : "teste2",
        "supplier_name" : "teste2",
        "cost" : 200,
        "component_type": "RAW",
        }]

    mock_session.query.return_value.filter.return_value.all.return_value = component_db

    response = client.get("/Components/get_all_components/",params= {"id": 1})

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body[0]["part_number"] == "teste"


def test_update_component_info_success(client: TestClient,
                                   mock_session):
    
    component_db = SimpleNamespace(
        id= 1,
        part_number = "teste",
        description = "teste",
        supplier_name = "teste",
        cost = 200,
        component_type = "RAW")
    
    payload = {"part_number" : "teste2"}

    mock_session.query.return_value.filter.return_value.first.return_value = component_db

    response = client.patch("/Components/update_component_info/teste", json=payload)

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Component updated successfuly"


def test_delete_component(client: TestClient, mock_session):

    component_db = SimpleNamespace(
        id= 1,
        part_number = "teste",
        description = "teste",
        supplier_name = "teste",
        cost = 200,
        component_type = "RAW")
    
    mock_session.query.return_value.filter.return_value.first.return_value = component_db

    response = client.delete("/Components/delete_component/teste")

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Component deleted successfuly"
























