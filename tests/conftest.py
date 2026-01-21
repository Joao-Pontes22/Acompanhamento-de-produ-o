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
from app.core.Settings.Settings import SECRET_KEY, ALGORITHM


# ===== FIXTURES =====

@pytest.fixture(scope="function")
def mock_session():
    """Cria um novo mock de sessão para cada teste."""
    return MagicMock()


@pytest.fixture(scope="function")
def client(mock_session) -> Generator:
    def override_init_session():
        yield mock_session

    app.dependency_overrides[Init_Session] = override_init_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def create_token():
    def _create_token(sub="testuser"):
        payload = {
            "sub": sub,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return _create_token
