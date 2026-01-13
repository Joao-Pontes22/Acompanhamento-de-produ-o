from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


def test_create_sector_success(client: TestClient, mock_session):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = None
    
    payload = {
        "sector": "Manufacturing",
        "tag": "MFG"
    }

    response = client.post("/sector/post_sector", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["sector"] == "Manufacturing"
    assert body["tag"] == "MFG"