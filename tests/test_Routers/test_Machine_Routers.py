from app.main import app
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def test_add_machine_success(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    sector_repo = MagicMock()
    sector_repo.repo_get_sector_by_id.return_value = {"ID": 1, "sector": "Manufacturing", "tag": "MFG"}

    with patch('app.Routes.Machine_Router.Sectors_repositorie', return_value=sector_repo):
        payload = {
            "machine": "Teste1",
            "sector_ID": 1,
            "description_machine": "Test description"
        }
        response = component.post("/Machine/POST_machine", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Machine created successfuly"

def test_get_all_machines_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "machine": "Teste1",
        "sector_ID": 1,
        "description_machine": "Test description"
    }

    mock_query = mock_session.query.return_value
    mock_query.all.return_value = [payload]

    response = component.get("/Machine/GET_machine")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["machine"] == "Teste1"
    assert body[0]["description_machine"] == "Test description"

def test_get_machine_by_id_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "machine": "Teste1",
        "sector_ID": 1,
        "description_machine": "Test description"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.get("/Machine/GET_machine_by_id", params={"id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["machine"] == "Teste1"
    assert body["description_machine"] == "Test description"

def test_get_machine_by_name_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "machine": "Teste1",
        "sector_ID": 1,
        "description_machine": "Test description"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.get("/Machine/GET_machine_by_name", params={"name": "Teste1"})

    assert response.status_code == 200
    body = response.json()
    assert body["machine"] == "Teste1"
    assert body["description_machine"] == "Test description"

def test_delete_machine_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "machine": "Teste1",
        "sector_ID": 1,
        "description_machine": "Test description"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.delete("/Machine/Delete_machine", params={"id": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Machine deleteded successfully"

def test_update_machine_success(component: TestClient, mock_session):
    # Usar um mock de objeto para simular o retorno do banco
    existing_machine = MagicMock()
    existing_machine.ID = 1
    existing_machine.machine = "Teste1"
    existing_machine.sector_ID = 1
    existing_machine.description_machine = "Test description"

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = existing_machine

    sector_repo = MagicMock()
    sector_repo.repo_get_sector_by_id.return_value = {"ID": 2, "sector": "Assembly", "tag": "ASM"}

    with patch('app.Routes.Machine_Router.Sectors_repositorie', return_value=sector_repo):
        payload = {
            "machine": "Teste1_Updated",
            "sector_ID": 2,
            "description_machine": "Updated description"
        }
        response = component.patch("/Machine/Update_machine", params={"id": 1}, json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Machine updated successfully"


# tests error

def test_add_machine_already_exists(component: TestClient, mock_session):   
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = {"ID": 1, "machine": "Teste1"}

    payload = {
        "machine": "Teste1",
        "sector_ID": 1,
        "description_machine": "Test description"
    }
    response = component.post("/Machine/POST_machine", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Machine already exist"

def test_delete_machine_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = component.delete("/Machine/Delete_machine", params={"id": 999})

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Machine not found"

def test_update_machine_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    payload = {
        "machine": "Teste1_Updated",
        "sector_ID": 2,
        "description_machine": "Updated description"
    }
    response = component.patch("/Machine/Update_machine", params={"id": 999}, json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Machine not found"

def test_add_machine_sector_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    sector_repo = MagicMock()
    sector_repo.repo_get_sector_by_id.return_value = None

    with patch('app.Routes.Machine_Router.Sectors_repositorie', return_value=sector_repo):
        payload = {
            "machine": "Teste1",
            "sector_ID": 999,
            "description_machine": "Test description"
        }
        response = component.post("/Machine/POST_machine", json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Sector not found"

def test_update_machine_sector_not_found(component: TestClient, mock_session):
    existing_machine = MagicMock()
    existing_machine.ID = 1
    existing_machine.machine = "Teste1"
    existing_machine.sector_ID = 1
    existing_machine.description_machine = "Test description"

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = existing_machine

    sector_repo = MagicMock()
    sector_repo.repo_get_sector_by_id.return_value = None

    with patch('app.Routes.Machine_Router.Sectors_repositorie', return_value=sector_repo):
        payload = {
            "machine": "Teste1_Updated",
            "sector_ID": 999,
            "description_machine": "Updated description"
        }
        response = component.patch("/Machine/Update_machine", params={"id": 1}, json=payload)

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Sector not found"


 