from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.domain.Exceptions import AlreadyExist, NotFoundException

def test_create_relation_success(component: TestClient, mock_session):
	mock_service = MagicMock()
	mock_service.service_create_relation.return_value = {"ID": 1, "part_ID": 1, "components_ID": 2, "qnty": 1}
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_Services', return_value=mock_service):
		response = component.post("/parts_to_components/create_relation", params={"part_ID": 1, "component_ID": 2})
	assert response.status_code == 200
	body = response.json()
	assert body["part_ID"] == 1
	assert body["components_ID"] == 2

def test_get_relations_by_part_success(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_relations_by_part_id.return_value = [
		{"ID": 1, "part_ID": 1, "components_ID": 2, "qnty": 1}
	]
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.get("/parts_to_components/relations_by_part/1")
	assert response.status_code == 200
	body = response.json()
	assert isinstance(body, list)
	assert body[0]["part_ID"] == 1

def test_delete_relation_success(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_relation_by_component_id.return_value = MagicMock()
	relation_repo.delete_relation.return_value = True
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.delete("/parts_to_components/delete_relation/1")
	assert response.status_code == 200
	body = response.json()
	assert body["message"] == "Relation deleted successfuly"

def test_get_all_relations_success(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_all_relations.return_value = [
		{"ID": 1, "part_ID": 1, "components_ID": 2, "qnty": 1},
		{"ID": 2, "part_ID": 1, "components_ID": 3, "qnty": 1}
	]
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.get("/parts_to_components/all_relations")
	assert response.status_code == 200
	body = response.json()
	assert isinstance(body, list)
	assert len(body) == 2


#tests errors

def test_get_relations_by_part_not_found(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_relations_by_part_id.return_value = []
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.get("/parts_to_components/relations_by_part/999")
	assert response.status_code == 404
	body = response.json()
	assert body["detail"] == "Relations not found"
	
def test_delete_relation_not_found(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_relation_by_component_id.return_value = None
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.delete("/parts_to_components/delete_relation/999")
	assert response.status_code == 404
	body = response.json()
	assert body["detail"] == "Relation not found"
	

def test_get_all_relations_not_found(component: TestClient, mock_session):
	relation_repo = MagicMock()
	relation_repo.get_all_relations.return_value = []
	with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_repositorie', return_value=relation_repo):
		response = component.get("/parts_to_components/all_relations")
	assert response.status_code == 404
	body = response.json()
	assert body["detail"] == "Relations not found"
	

def test_create_relation_already_exists(component: TestClient, mock_session):
    mock_service = MagicMock()
    mock_service.service_create_relation.side_effect = AlreadyExist("Relation")
    with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_Services', return_value=mock_service):
        response = component.post("/parts_to_components/create_relation", params={"part_ID": 1, "component_ID": 2})
    assert response.status_code == 409
    body = response.json()
    assert body["detail"] == "Relation already exist"


def test_create_relation_component_not_found(component: TestClient, mock_session):
    mock_service = MagicMock()
    mock_service.service_create_relation.side_effect = NotFoundException("Component")
    with patch('app.Routes.RelationPartsxComponents_Router.RelationPartsxComponents_Services', return_value=mock_service):
        response = component.post("/parts_to_components/create_relation", params={"part_ID": 1, "component_ID": 999})
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Component not found"



