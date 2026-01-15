from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
import pytest
from main import app
from app.core.Dependecies import Init_Session
from typing import Generator
from unittest.mock import MagicMock
from app.core.Settings.Settings import SECRET_KEY, ALGORITHM
from jose import jwt
# REMOVA o mock_session global daqui

@pytest.fixture(scope="function")
def mock_session():
    """Cria um novo mock para cada teste individualmente."""
    return MagicMock()

@pytest.fixture(scope="function")
def client(mock_session) -> Generator:
    # Função interna para injetar o mock específico deste teste
    def override_init_Session():
        try:
            yield mock_session
        finally:
            pass

    app.dependency_overrides[Init_Session] = override_init_Session
    with TestClient(app) as c:
        yield c
    
    # Limpa as substituições para não afetar outros testes
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def component(mock_session) -> Generator:
    # Função interna para injetar o mock específico deste teste
    def override_init_Session():
        try:
            yield mock_session
        finally:
            pass

    app.dependency_overrides[Init_Session] = override_init_Session
    with TestClient(app) as c:
        yield c
    
    # Limpa as substituições para não afetar outros testes
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def employer(mock_session) -> Generator:
    # Função interna para injetar o mock específico deste teste
    def override_init_Session():
        try:
            yield mock_session
        finally:
            pass

    app.dependency_overrides[Init_Session] = override_init_Session
    with TestClient(app) as c:
        yield c
    
    # Limpa as substituições para não afetar outros testes
    app.dependency_overrides.clear()

@pytest.fixture
def create_token_fixture():
    def _create_token(sub="testuser"):
        payload = {
            "sub": sub,
            "exp": datetime.now(timezone.utc) + timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    return _create_token