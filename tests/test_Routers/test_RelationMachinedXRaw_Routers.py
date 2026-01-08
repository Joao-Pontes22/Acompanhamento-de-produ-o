
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def test_add_relation_success(component: TestClient, mock_session):
    # Mock dos componentes existentes
    mock_component1 = MagicMock()
    mock_component2 = MagicMock()
    components_repo = MagicMock()
    components_repo.repo_get_Component_by_id.side_effect = [mock_component1, mock_component2]

    # Mock do repo de relação para não existir relação prévia
    relation_repo = MagicMock()
    relation_repo.get_relation_by_machined_id.return_value = None
    relation_repo.create_relation.return_value = MagicMock()

    # Patcha o repositório de componentes e de relação no router
    from unittest.mock import patch
    payload = {
        "raw_component_id": 1,
        "machined_component_id": 2,
        "qnty": 1
    }
    with patch('app.Routes.RelationMachinedXRaw_Router.Components_Repositorie', return_value=components_repo), \
         patch('app.Routes.RelationMachinedXRaw_Router.RelationMachinedxRaw_repositorie', return_value=relation_repo):
        response = component.post("/RelationMachinedXRaw/add_relation", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Relation created successfuly"


def test_get_relation_by_machined_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "raw_ID": 1,
        "machined_ID": 2,
        "qnty": 1
    }

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = payload

    response = component.get("/RelationMachinedXRaw/get_relation_by_machined/2")

    assert response.status_code == 200
    body = response.json()
    assert body["machined_ID"] == 2
    assert body["raw_ID"] == 1


def test_get_relation_by_raw_success(component: TestClient, mock_session):
    # Mock the component returned by the repo
    mock_component = MagicMock()
    mock_component.id = 1
    components_repo = MagicMock()
    components_repo.repo_get_Component_by_id.return_value = mock_component

    # Mock the relation returned by the query
    relation = {
        "ID": 1,
        "raw_ID": 1,
        "machined_ID": 2,
        "qnty": 1
    }
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = relation

    with patch('app.Routes.RelationMachinedXRaw_Router.Components_Repositorie', return_value=components_repo):
        response = component.get("/RelationMachinedXRaw/get_relation_by_raw/1")

    assert response.status_code == 200
    body = response.json()
    assert body["machined_ID"] == 2
    assert body["raw_ID"] == 1

def test_delete_relation_success(component: TestClient, mock_session):
    # Mock the component returned by the repo
    mock_component = MagicMock()
    mock_component.id = 2
    components_repo = MagicMock()
    components_repo.repo_get_Component_by_part_number.return_value = mock_component

    # Mock the relation returned by the query
    relation = MagicMock()
    relation.id = 1
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = relation

    with patch('app.Routes.RelationMachinedXRaw_Router.Components_Repositorie', return_value=components_repo):
        response = component.delete("/RelationMachinedXRaw/delete_relation/2")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Relation deleted successfuly"

def test_get_all_relations_success(component: TestClient, mock_session):
    payload = {
        "ID": 1,
        "raw_ID": 1,
        "machined_ID": 2,
        "qnty": 1
    }

    mock_query = mock_session.query.return_value
    mock_query.all.return_value = [payload]

    response = component.get("/RelationMachinedXRaw/get_all_relations")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["machined_ID"] == 2
    assert body[0]["raw_ID"] == 1


# errors tests

def test_add_relation_component_not_found(component: TestClient, mock_session):
    # Mock dos componentes inexistentes
    components_repo = MagicMock()
    components_repo.repo_get_Component_by_id.side_effect = [None, None]
    
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None
    # Patcha o repositório de componentes no router
    from unittest.mock import patch
    payload = {
        "raw_component_id": 1,
        "machined_component_id": 2,
        "qnty": 1
    }
    with patch('app.Routes.RelationMachinedXRaw_Router.Components_Repositorie', return_value=components_repo):
        response = component.post("/RelationMachinedXRaw/add_relation", json=payload)
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Component not found"


def test_add_relation_already_exists(component: TestClient, mock_session):
    # Mock dos componentes existentes
    mock_component1 = MagicMock()
    mock_component2 = MagicMock()
    components_repo = MagicMock()
    components_repo.repo_get_Component_by_id.side_effect = [mock_component1, mock_component2]

    # Mock do repo de relação para já existir relação prévia
    relation_repo = MagicMock()
    relation_repo.get_relation_by_machined_id.return_value = MagicMock()

    # Patcha o repositório de componentes e de relação no router
    from unittest.mock import patch
    payload = {
        "raw_component_id": 1,
        "machined_component_id": 2,
        "qnty": 1
    }
    with patch('app.Routes.RelationMachinedXRaw_Router.Components_Repositorie', return_value=components_repo), \
         patch('app.Routes.RelationMachinedXRaw_Router.RelationMachinedxRaw_repositorie', return_value=relation_repo):
        response = component.post("/RelationMachinedXRaw/add_relation", json=payload)
    assert response.status_code == 409
    body = response.json()
    assert body["detail"] == "Relation already exist"

def test_get_relation_by_machined_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None

    response = component.get("/RelationMachinedXRaw/get_relation_by_machined/999")

    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Relation not found"