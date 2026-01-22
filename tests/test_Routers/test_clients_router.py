from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from types import SimpleNamespace


def test_create_client_success(client: TestClient, mock_session):
    # Arrange
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    payload = {
        "name": "Teste",
        "contact": "Teste",
        "email": "teste@gmail.com",
        "phone": "14932948"
    }

    # Act
    response = client.post("/Clients/create_client", json=payload)

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Client created successfuly"
    assert body["Client"] == "TESTE"

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_all_clients_success(client: TestClient, mock_session):
    client_db = [{
                    "name": "Teste",
                    "contact": "Teste",
                    "email": "teste@gmail.com",
                    "phone": "14932948"
                }, 
                {
                        "name": "Teste2",
                        "contact": "Teste2",
                        "email": "teste2@gmail.com",
                        "phone": "149329428"
                }]
    mock_session.query.return_value.all.return_value = client_db
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    response = client.get("/Clients/get_all_clients")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["name"] == "Teste"
    assert body[1]["name"] == "Teste2"


def test_get_clients_by_name_success(client: TestClient, mock_session):
    # Arrange
    client_db = SimpleNamespace(
        name="Teste",
        contact="Teste",
        email="teste@gmail.com",
        phone="14932948"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = client_db

    # Act
    response = client.get("/Clients/get_by_name/Teste")

    # Assert
    assert response.status_code == 200

    body = response.json()
    assert body["name"] == "Teste"
    assert body["email"] == "teste@gmail.com"


def test_update_client_info_success(client: TestClient, mock_session):
    # Arrange
    client_db = SimpleNamespace(
        name="Teste",
        contact="Teste",
        email="teste@gmail.com",
        phone="14932948"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = client_db
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    payload = {
        "name": "Teste2"
    }

    # Act
    response = client.patch("/Clients/update_client_by_name/Teste", json=payload)

    # Assert
    assert response.status_code == 200

    body = response.json()
    assert body["name"] == "TESTE2"
    assert body["email"] == "teste@gmail.com"


def test_delete_client_success(client: TestClient, mock_session):
    # Arrange
    client_db = SimpleNamespace(
        name="Teste",
        contact="Teste",
        email="teste@gmail.com",
        phone="14932948"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = client_db
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None



    # Act
    response = client.delete("/Clients/delete_client/Teste")

    # Assert
    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Client deleted successfuly"


#Exceptions 

def test_create_client_already_exist_exception(client: TestClient, mock_session):

    client_db = SimpleNamespace(
        name="Teste",
        contact="Teste",
        email="teste@gmail.com",
        phone="14932948"
    )
    # Arrange
    mock_session.query.return_value.filter.return_value.first.return_value = client
    mock_session.commit.return_value = None

    payload = {
        "name": "Teste",
        "contact": "Teste",
        "email": "teste@gmail.com",
        "phone": "14932948"
    }

    # Act
    response = client.post("/Clients/create_client", json=payload)

    # Assert
    assert response.status_code == 409

    body = response.json()

    assert body["detail"] == "TESTE already exist"


def test_get_all_clients_not_found_exception(client: TestClient, mock_session):
  
    mock_session.query.return_value.all.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    response = client.get("/Clients/get_all_clients")

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Clients not found"


def test_get_clients_by_name_not_found_exception(client: TestClient, mock_session):
   

    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.get("/Clients/get_by_name/Teste")

    # Assert
    assert response.status_code == 404

    body = response.json()
    assert body["detail"] == "Client not found"


def test_update_client_info_not_found_exception(client: TestClient, mock_session):
    

    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    payload = {
        "name": "Teste2"
    }

    # Act
    response = client.patch("/Clients/update_client_by_name/Teste", json=payload)

    # Assert
    assert response.status_code == 404

    body = response.json()
    assert body["detail"] == "Client not found"


def test_delete_client_not_found_exception(client: TestClient, mock_session):
   

    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None



    # Act
    response = client.delete("/Clients/delete_client/Teste")

    # Assert
    assert response.status_code == 404

    body = response.json()
    assert body["detail"] == "Client not found"    
