from main import app
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def test_add_part_success(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    clients_repo = MagicMock()
    clients_repo.repo_get_client_by_id.return_value = {"ID": 1, "name": "Client A", "contact": "contact@example.com"}
    with patch('app.Routes.Parts_Router.Clients_repositorie', return_value=clients_repo):
        payload = {
            "part_number": "P12345",
            "description": "Test Part",
            "client_ID": 1,
            "cost": 99.99
        }
        response = component.post("/Parts/add_parts", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Part created successfuly"

def test_get_all_parts_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "part_number": "P12345",
        "description": "Test Part",
        "client_ID": 1,
        "cost": 99.99
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.all.return_value = [payload]

    response = component.get("/Parts/get_parts")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["part_number"] == "P12345"
    assert body[0]["description"] == "Test Part"

def test_get_part_by_id_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "part_number": "P12345",
        "description": "Test Part",
        "client_ID": 1,
        "cost": 99.99
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.get("/Parts/Get_parts_by_id", params={"id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["part_number"] == "P12345"
    assert body["description"] == "Test Part"

def test_get_part_by_part_number_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "part_number": "P12345",
        "description": "Test Part",
        "client_ID": 1,
        "cost": 99.99
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.get("/Parts/Get_parts_by_part_number", params={"part_number": "P12345"})

    assert response.status_code == 200
    body = response.json()
    assert body["part_number"] == "P12345"
    assert body["description"] == "Test Part"

def test_delete_part_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "part_number": "P12345",
        "description": "Test Part",
        "client_ID": 1,
        "cost": 99.99
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.delete("/Parts/Delete_part", params={"id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Part deleteded successful"

def test_update_part_success(component: TestClient, mock_session):
    partORM = MagicMock()
    partORM.id = 1
    partORM.part_number = "P12345"
    partORM.description = "Test Part"
    partORM.client_ID = 1
    partORM.cost = 99.99

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = partORM

    update_payload = {
        "part_number": "P54321",
        "description_parts": "Updated Test Part",
        "client_ID": 1,
        "cost": 149.99
    }

    response = component.patch("/Parts/update_part/1", json=update_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Parts updated successfuly"

#errors tests
def test_add_part_already_exists(component: TestClient, mock_session):
    existing_part = {
        "ID": 1,
        "part_number": "P12345",
        "description": "Existing Part",
        "client_ID": 1,
        "cost": 99.99
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = existing_part

    clients_repo = MagicMock()
    clients_repo.repo_get_client_by_id.return_value = {"ID": 1, "name": "Client A", "contact": "test@example.com"}

    with patch('app.Routes.Parts_Router.Clients_repositorie', return_value=clients_repo):
        payload = {
            "part_number": "P12345",
            "description": "Test Part",
            "client_ID": 1,
            "cost": 99.99
        }
        response = component.post("/Parts/add_parts", json=payload)
    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Part already exist"


def test_get_part_by_id_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = component.get("/Parts/Get_parts_by_id", params={"id": 999})

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Part not found"

def test_get_part_by_part_number_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = component.get("/Parts/Get_parts_by_part_number", params={"part_number": "NONEXISTENT"})

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Part not found"

def test_delete_part_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = component.delete("/Parts/Delete_part", params={"id": 999})

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Part not found"

def test_update_part_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    payload = {
        "part_number": "P54321",
        "description_parts": "Updated Test Part",
        "client_ID": 1,
        "cost": 149.99
    }
    response = component.patch("/Parts/update_part/999", json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Part not found"

def test_add_part_client_not_found(component: TestClient, mock_session):   
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    clients_repo = MagicMock()
    clients_repo.repo_find_clients_by_id.return_value = None
    with patch('app.Routes.Parts_Router.Clients_repositorie', return_value=clients_repo):
        payload = {
            "part_number": "P12345",
            "description": "Test Part",
            "client_ID": 999,
            "cost": 99.99
        }
        response = component.post("/Parts/add_parts", json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Customer not found"


def test_update_part_client_not_found(component: TestClient, mock_session):
    partORM = MagicMock()
    partORM.id = 1
    partORM.part_number = "P12345"
    partORM.description = "Test Part"
    partORM.client_ID = 1
    partORM.cost = 99.99

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = partORM

    clients_repo = MagicMock()
    clients_repo.repo_find_clients_by_id.return_value = None

    with patch('app.Routes.Parts_Router.Clients_repositorie', return_value=clients_repo):
        payload = {
            "part_number": "P54321",
            "description_parts": "Updated Test Part",
            "client_ID": 999,
            "cost": 149.99
        }
        response = component.patch("/Parts/update_part/1", json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Customer not found"



