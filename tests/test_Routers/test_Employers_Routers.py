from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app



def test_add_employer_success(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    sectors_mock = MagicMock()
    sectors_mock.repo_get_sector_by_id.return_value = {"ID": 1, "name": "IT"}

    payload = {
        "name": "Test",
        "sector_ID": 1,
        "password": "123",
        "emp_id": "EMP123"
    }

    with patch('app.Routes.Employer_Router.Sectors_repositorie', return_value=sectors_mock):
        response = employer.post("/Employers/Create_Employer", json=payload)

    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Employer created successful"

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_get_all_employers_success(employer: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TEST",
        "sector_ID": 1,
        "emp_id": "EMP123"
    }

    mock_query = mock_session.query.return_value
    mock_query.all.return_value = [payload]

    response = employer.get("/Employers/get_employers")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["name"] == "TEST"
    assert body[0]["emp_id"] == "EMP123"

def test_get_employer_by_emp_id_success(employer: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TEST",
        "sector_ID": 1,
        "emp_id": "EMP123"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = employer.get("/Employers/GET_Employer_By_Emp_ID/EMP123")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "TEST"
    assert body["emp_id"] == "EMP123"

def test_delete_employer_success(employer: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TEST",
        "sector_ID": 1,
        "emp_id": "EMP123"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = employer.delete("/Employers/Delete_employer/1")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Employer deleted successfuly"

def test_get_employer_by_id_success(employer: TestClient, mock_session):
    payload = {
        "ID": 1,
        "name": "TEST",
        "sector_ID": 1,
        "emp_id": "EMP123"
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = employer.get("/Employers/Get_employer_by_id/1")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "TEST"
    assert body["emp_id"] == "EMP123"



# test errors

def test_add_employer_already_exists(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = {"ID": 1, "name": "TEST"}

    payload = {
        "name": "Test",
        "sector_ID": 1,
        "password": "123",
        "emp_id": "EMP123"
    }

    response = employer.post("/Employers/Create_Employer", json=payload)

    assert response.status_code == 409

    body = response.json()
    assert body["detail"] == "Employer already exist"

def test_get_all_employers_not_found(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.all.return_value = None

    response = employer.get("/Employers/get_employers")

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Employers not found"

def test_get_employer_by_emp_id_not_found(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = employer.get("/Employers/GET_Employer_By_Emp_ID/EMP123")

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_delete_employer_not_found(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = employer.delete("/Employers/Delete_employer/1")

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_get_employer_by_id_not_found(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = employer.get("/Employers/Get_employer_by_id/1")

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Employer not found"

def test_add_employer_sector_not_found(employer: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    sectors_mock = MagicMock()
    sectors_mock.repo_get_sector_by_id.return_value = None

    payload = {
        "name": "Test",
        "sector_ID": 99,
        "password": "123",
        "emp_id": "EMP123"
    }

    with patch('app.Routes.Employer_Router.Sectors_repositorie', return_value=sectors_mock):
        response = employer.post("/Employers/Create_Employer", json=payload)

    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Sector not found"