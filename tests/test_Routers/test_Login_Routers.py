from main import app
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.core.Settings.Settings import ALGORITHM, bcrypt_context, SECRET_KEY
from jose import jwt

# Success tests
def test_Login_success(client: TestClient, mock_session):
    user_mock = MagicMock()
    user_mock.ID = 1
    user_mock.emp_id = "TESTUSER"
    user_mock.password = bcrypt_context.hash("TESTPASS")  # Ou hash, se for o caso
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = user_mock

    payload = {"emp_id": "TESTUSER", "password": "TESTPASS"}
    response = client.post("/Login/Login", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] is not None
    assert body["token_type"] == "bearer"

def test_Login_form_success(client: TestClient, mock_session):
    user_mock = MagicMock()
    user_mock.ID = 1
    user_mock.emp_id = "TESTUSER"
    user_mock.password = bcrypt_context.hash("TESTPASS")  # Ou hash, se for o caso
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = user_mock

    payload = {"username": "TESTUSER", "password": "TESTPASS"}
    response = client.post("/Login/Login_Form", data=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] is not None
    assert body["token_type"] == "bearer"


def test_Refresh_token_success(client: TestClient,create_token_fixture):
    token = create_token_fixture(sub="TESTUSER")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/Login/Refresh_Token/TESTUSER", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] is not None
    assert body["token_type"] == "bearer"

# Failure tests
def test_Login_user_not_found(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    payload = {"emp_id": "NONEXISTENT", "password": "ANYPASS"}
    response = client.post("/Login/Login", json=payload)
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_Login_incorrect_password(client: TestClient, mock_session):
    user_mock = MagicMock()
    user_mock.ID = 1
    user_mock.emp_id = "TESTUSER"
    user_mock.password = bcrypt_context.hash("CORRECTPASS")
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = user_mock

    payload = {"emp_id": "TESTUSER", "password": "WRONGPASS"}
    response = client.post("/Login/Login", json=payload)
    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Password incorrect"

def test_Login_form_user_not_found(client: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    payload = {"username": "NONEXISTENT", "password": "ANYPASS"}
    response = client.post("/Login/Login_Form", data=payload)
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_Login_form_incorrect_password(client: TestClient, mock_session):
    user_mock = MagicMock()
    user_mock.ID = 1
    user_mock.emp_id = "TESTUSER"
    user_mock.password = bcrypt_context.hash("CORRECTPASS")
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = user_mock

    payload = {"username": "TESTUSER", "password": "WRONGPASS"}
    response = client.post("/Login/Login_Form", data=payload)
    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Password incorrect"

def test_Refresh_token_user_not_found(client: TestClient, create_token_fixture, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    token = create_token_fixture(sub="TESTUSER")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/Login/Refresh_Token/TESTUSER", headers=headers)
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_Refresh_token_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.post("/Login/Refresh_Token/TESTUSER", headers=headers)
    assert response.status_code == 401
    body = response.json()
    assert body["detail"] == "Invalid token"