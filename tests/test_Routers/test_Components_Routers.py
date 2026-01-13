from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch


# tests succes

def test_add_components_success(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.side_effect = [
        None, 
        MagicMock(id=1, name="Fornecedor Fixo")
    ]
    
    payload = {
        "part_number": "car-001-BR",
        "description" : "Carcaça de direção",
        "supplier" : "Fornecedor Fixo",
        "cost" : 200
    }

    with patch('app.Routes.Components_Router.Suppliers_Repositorie'):
        response = component.post("/Components/add_component", json=payload)
        
        assert response.status_code == 200
        body = response.json()
        assert body["message"] == "Component created successful"
        assert body["Component"] == "CAR-001-BR"

def test_get_all_components_success(component: TestClient, mock_session):
    payload = [{
        "id": 1,
        "part_number": "CAR-001-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier" : "Fornecedor Fixo",
        "category": "COMPONENT",
        "cost" : 200
    }]

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = payload

    response = component.get("/Components/Get_all_Components")

    assert response.status_code == 200
    body = response.json()
    assert body[0]["part_number"] == "CAR-001-BR"
    assert body[0]["description"] == "CARCAÇA DE DIREÇÃO"

def test_get_filtered_by_id_components_success(component: TestClient, mock_session):
    payload = [{
        "id": 1,
        "part_number": "CAR-001-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier" : "Fornecedor Fixo",
        "category": "COMPONENT",
        "cost" : 200
    }, 
    {
        "id": 2,
        "part_number": "CAR-002-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier" : "Fornecedor Fixo",
        "category": "COMPONENT",
        "cost" : 200
    }]

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = payload

    response = component.get("/Components/get_components_filtered", params= { "id": 1
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body[0]["part_number"] == "CAR-001-BR"
    assert body[0]["description"] == "CARCAÇA DE DIREÇÃO"

def test_get_filtered_by_part_number_components_success(component: TestClient, mock_session):
    payload = [{
        "id": 1,
        "part_number": "CAR-001-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier_ID" : 1,
        "category": "COMPONENT",
        "cost" : 200
    }, 
    {
        "id": 2,
        "part_number": "CAR-002-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier_ID" : 2,
        "category": "COMPONENT",
        "cost" : 200
    }]

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = payload

    response = component.get("/Components/get_components_filtered", params= { "part_number": "CAR-001-BR"
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body[0]["part_number"] == "CAR-001-BR"
    assert body[0]["description"] == "CARCAÇA DE DIREÇÃO"

def test_get_filtered_by_supplier_id_components_success(component: TestClient, mock_session):
    payload = [{
        "id": 1,
        "part_number": "CAR-001-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier" : "Fornecedor Fixo",
        "category": "COMPONENT",
        "cost" : 200
    }, 
    {
        "id": 2,
        "part_number": "CAR-002-BR",
        "description" : "CARCAÇA DE DIREÇÃO",
        "supplier" : "Fornecedor Fixo 2",
        "category": "COMPONENT",
        "cost" : 200
    }]

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = payload

    response = component.get("/Components/get_components_filtered", params= { "supplier_ID": 2
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert body[1]["part_number"] == "CAR-002-BR"
    assert body[1]["description"] == "CARCAÇA DE DIREÇÃO"

def test_update_components_infos_success(component: TestClient, mock_session):
    # --- Criando um mock para o componente existente (ORM) ---
    component_orm = MagicMock(
        id=1,
        part_number="CAR-001-BR",
        description="CARCAÇA DE DIREÇÃO",
        supplier_ID=1,
        category="COMPONENT",
        cost=200
    )

    # --- Criando um mock para o novo fornecedor ---
    supplier_orm = MagicMock(id=3, name="Fornecedor Atualizado")

    # --- Configurando o mock do session para simular busca do componente ---
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = component_orm

    # --- Mockando o repositório de fornecedores ---
    supplier_repo_mock = MagicMock()
    supplier_repo_mock.repo_get_suplier_by_id.return_value = supplier_orm

    # --- Usando patch para substituir a classe de repositório no escopo do teste ---
    with patch('app.Routes.Components_Router.Suppliers_Repositorie', return_value=supplier_repo_mock):
        request = {"part_number": "CAR-002-BR", "supplier_ID": 3}
        response = component.patch("/Components/update_component_info/1", json=request)

        # --- Asserções ---
        assert response.status_code == 200
        body = response.json()
        assert body["part_number"] == "CAR-002-BR"
        assert body["description"] == "CARCAÇA DE DIREÇÃO"

def test_delete_components_success(component: TestClient, mock_session):
    Component = MagicMock(
        id=1,
        part_number="CAR-001-BR",
        description="CARCAÇA DE DIREÇÃO",)

    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = Component

    response = component.delete("/Components/Delete_component/1")

    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Component deleted successfuly"

#tests errors

def test_add_components_error_supplier_not_exist(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.side_effect = [
        None, 
        None 
    ]
    
    payload = {
        "part_number": "car-001-BR",
        "description" : "Carcaça de direção",
        "supplier_ID" : 99, 
        "cost" : 200
    }

    supplier_repo_mock = MagicMock()
    supplier_repo_mock.repo_get_suplier_by_id.return_value = None

    with patch('app.Routes.Components_Router.Suppliers_Repositorie', return_value=supplier_repo_mock):
        response = component.post("/Components/add_component", json=payload)
        
        assert response.status_code == 400
        body = response.json()
        assert body["detail"] == "Supplier not found"

def test_update_components_infos_error_cost_invalid(component: TestClient, mock_session):
    component_orm = MagicMock()
    component_orm.id = 1
    component_orm.part_number = "CAR-001-BR"
    component_orm.description = "CARCAÇA DE DIREÇÃO"
    component_orm.supplier_ID = 1
    component_orm.category = "COMPONENT"
    component_orm.cost = 200

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = component_orm

    supplier_repo_mock = MagicMock()
    supplier_repo_mock.repo_get_suplier_by_id.return_value = MagicMock(id=1)

    with patch('app.Routes.Components_Router.Suppliers_Repositorie', return_value=supplier_repo_mock):
        request = {"cost": -50} 
        response = component.patch("/Components/update_component_info/1", json=request)

        assert response.status_code == 409
        body = response.json()
        assert body["detail"] == "Cost must be greater than zero"

def test_update_component_not_found(component: TestClient, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = None 

    supplier_repo_mock = MagicMock()

    with patch('app.Routes.Components_Router.Suppliers_Repositorie', return_value=supplier_repo_mock):
        request = {"part_number": "CAR-002-BR"}
        response = component.patch("/Components/update_component_info/999", json=request)

        assert response.status_code == 400
        body = response.json()
        assert body["detail"] == "Component not found"
    component_orm = MagicMock()
    component_orm.id = 1
    component_orm.part_number = "CAR-001-BR"
    component_orm.description = "CARCAÇA DE DIREÇÃO"
    component_orm.supplier_ID = 1
    component_orm.category = "COMPONENT"
    component_orm.cost = 200

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = component_orm

def test_update_component_error_supplier_notfound(component: TestClient):
    supplier_repo_mock = MagicMock()
    supplier_repo_mock.repo_get_suplier_by_id.return_value = None

    with patch('app.Routes.Components_Router.Suppliers_Repositorie', return_value=supplier_repo_mock):
        request = {"part_number": "CAR-002-BR",
                   "supplier_ID": 4}
        response = component.patch("/Components/update_component_info/1", json=request)

        assert response.status_code == 400
        body = response.json()
        assert body["detail"] == "Supplier not found"

def test_delete_components_error_not_found(component: TestClient, mock_session):
    Component = MagicMock()

    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    response = component.delete("/Components/Delete_component/1")

    assert response.status_code == 400

    body = response.json()
    assert body["detail"] == "Component not found"




