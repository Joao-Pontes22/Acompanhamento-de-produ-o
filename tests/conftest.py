# ===== AJUSTE DE PATH (TEM QUE SER O PRIMEIRO) =====
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# ===== IMPORTS NORMAIS =====
from datetime import datetime, timedelta, timezone
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from main import app
from app.core.Dependecies import Init_Session
from app.repositories.Suppliers_repository import SuppliersRepository
from app.core.Settings.Settings import SECRET_KEY, ALGORITHM


# ===== FIXTURES =====

@pytest.fixture(scope="function")
def mock_session():
    """Cria um novo mock de sessão para cada teste."""
    return MagicMock()


@pytest.fixture(scope="function")
def client(mock_session, mock_supplier_repo) -> Generator:
    def override_init_session():
        yield mock_session
    def override_SupplierRepo():
        yield mock_supplier_repo
    app.dependency_overrides[Init_Session] = override_init_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def mock_supplier_repo():
    return MagicMock()

@pytest.fixture
def mock_employer_repo():
    return MagicMock()

@pytest.fixture
def mock_client_repo():
    return MagicMock()

@pytest.fixture
def mock_machine_repo():
    return MagicMock()

@pytest.fixture
def mock_relation_repo():
    return MagicMock()

@pytest.fixture
def mock_machining_repo():
    return MagicMock()

@pytest.fixture
def mock_movimentation_repo():
    return MagicMock()

@pytest.fixture
def mock_parts_repo():
    return MagicMock()

@pytest.fixture
def mock_sector_repo():
    return MagicMock()

@pytest.fixture
def mock_stock_repo():
    return MagicMock()


@pytest.fixture
def create_token():
    def _create_token(sub="testuser"):
        payload = {
            "sub": sub,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return _create_token
