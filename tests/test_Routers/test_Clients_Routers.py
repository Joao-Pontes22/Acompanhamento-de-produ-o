from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock


# Success tests
def test_add_client_success(client: TestClient, mock_session):

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None
    mock_query.filter_by.return_value.first.return_value = None

    payload = {
        "name": "Teste",
        "contact": "Teste@gmail.com",
        "email": "Teste@gmail.com",
        "phone": "159883672"
    }

    response = client.post("/Clients/add_client", json=payload)

    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Client created successfuly"
    assert body["Client"] == "TESTE"

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_get_all_clients_success(client: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TESTE",
        "contact": "TESTE@GMAIL.COM",
        "email": "Teste@gmail.com",
        "phone": "159883672"
    }

    mock_query = mock_session.query.return_value
    mock_query.all.return_value = [payload]

    response = client.get("/Clients/get_all_clients")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["name"] == "TESTE"
    assert body[0]["contact"] == "TESTE@GMAIL.COM"

def test_get_client_by_name_success(client: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TESTE",
        "contact": "TESTE@GMAIL.COM",
        "email": "Teste@gmail.com",
        "phone": "159883672"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = client.get("/Clients/get_by_name/TESTE")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "TESTE"
    assert body["contact"] == "TESTE@GMAIL.COM"

def test_patch_client_success(client: TestClient, mock_session):
    client_db = MagicMock()
    client_db.id = 1
    client_db.name = "OLD NAME"
    client_db.contact = "OLD@EMAIL.COM"
    client_db.email = "old@gmail.com"
    client_db.phone = "111111"

    updated_payload = {
        "name": "NEW NAME",
        "email": "new@gmail.com"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = client_db

    response = client.patch(
        "/Clients/update_client_by_name/OLD NAME",
        json=updated_payload
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "NEW NAME"
    assert body["email"] == "new@gmail.com"

def test_delete_client_succes(client: TestClient, mock_session):
    client_db = MagicMock()
    client_db.ID = 1
    mock_query = mock_session.query.return_value 
    mock_query.filter.return_valuefirst.return_value = client_db

    response = client.delete("/Clients/Delete_client/1")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Client deleted successfuly"


# Erros tests

def test_add_client_error_alreadyexist(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value 
    mock_query.filter.return_value 
    mock_query.first.return_value = MagicMock(name="TOYOTA")

    payload = {
        "name": "Toyota",
        "contact": "Toyota@gmail.com",
        "email": "Toyota@gmail.com",
        "phone": "159883672"
    }

    response = client.post("/Clients/add_client", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "TOYOTA already exist"

    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

def test_add_client_error_less3caracteresError(client: TestClient, mock_session):

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None
    mock_query.filter_by.return_value.first.return_value = None

    payload = {
        "name": "Te",
        "contact": "Teste@gmail.com",
        "email": "Teste@gmail.com",
        "phone": "159883672"
    }

    response = client.post("/Clients/add_client", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Name must be grather than 3 caracteres"

def test_get_all_clients_error_notfound(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.all.return_value = None

    response = client.get("/Clients/Get_all_clients")

    assert response.status_code == 404
    body = response.json()

    assert body["detail"] == "Clients not found"

def test_get_client_by_id_error_notfound(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = client.get("/Clients/Get_by_ID/1")

    assert response.status_code == 404
    body = response.json()

    assert body["detail"] == "Client not found"

def test_patch_client_error_less3caracteres(client: TestClient, mock_session):
    client_db = MagicMock()
    client_db.id = 1
    client_db.name = "OLD NAME"
    client_db.contact = "OLD@EMAIL.COM"
    client_db.email = "old@gmail.com"
    client_db.phone = "111111"

    updated_payload = {
        "name": "NE",
        "email": "new@gmail.com"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = client_db

    response = client.patch(
        "/Clients/update_client_by_id/1",
        json=updated_payload
    )

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Name must be grather than 3 caracteres"

def test_delete_client_error_not_found(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value 
    mock_query.filter.return_value.first.return_value = None
    response = client.delete("/Clients/Delete_client/1")

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Client not found"  

def test_patch_client_error_not_found(client: TestClient, mock_session):
    updated_payload = {
        "name": "NEW NAME",
        "email": "new@gmail.com"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = client.patch(
        "/Clients/update_client_by_id/2",
        json=updated_payload
    )

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Client not found"

