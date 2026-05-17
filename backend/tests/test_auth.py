"""
Módulo: tests/test_auth.py
Responsabilidad: casos de prueba para el endpoint de login/logout.
Trazabilidad: REQ-NF02
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
import importlib


def make_auth_mock(success=True):
    """Construye un mock del cliente Supabase para auth."""
    mock_session = MagicMock()
    mock_session.access_token = "fake-jwt-token-123"
    mock_user = MagicMock()
    mock_user.email = "admin@autobhan.com"

    mock_result = MagicMock()
    mock_result.session = mock_session if success else None
    mock_result.user = mock_user if success else None

    mock_auth = MagicMock()
    mock_auth.sign_in_with_password.return_value = mock_result
    mock_auth.sign_out.return_value = None

    mock_client = MagicMock()
    mock_client.auth = mock_auth
    return mock_client


# ── REQ-NF02 ─────────────────────────────────────────────────────────────────

@pytest.mark.REQ_NF02
def test_login_exitoso():
    """
    TC-018: POST /auth/login con credenciales válidas retorna 200 y token JWT.

    Trazabilidad: REQ-NF02
    """
    mock_client = make_auth_mock(success=True)
    with patch("db.supabase_client.supabase", mock_client):
        for mod in list(sys.modules.keys()):
            if mod.startswith(("routers", "main")):
                del sys.modules[mod]
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        with patch("routers.auth._get_db", return_value=mock_client):
            response = client.post("/auth/login", json={
                "email": "admin@autobhan.com",
                "password": "password123",
            })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_email"] == "admin@autobhan.com"


@pytest.mark.REQ_NF02
def test_login_credenciales_invalidas():
    """
    TC-019: POST /auth/login con credenciales incorrectas retorna 401.

    Trazabilidad: REQ-NF02
    """
    mock_client = make_auth_mock(success=False)
    with patch("db.supabase_client.supabase", mock_client):
        for mod in list(sys.modules.keys()):
            if mod.startswith(("routers", "main")):
                del sys.modules[mod]
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        with patch("routers.auth._get_db", return_value=mock_client):
            response = client.post("/auth/login", json={
                "email": "admin@autobhan.com",
                "password": "wrong-password",
            })
    assert response.status_code == 401
    assert "Credenciales inválidas" in response.json()["detail"]


@pytest.mark.REQ_NF02
def test_login_email_invalido():
    """
    TC-020: POST /auth/login con email malformado retorna 422.

    Trazabilidad: REQ-NF02
    """
    mock_client = make_auth_mock(success=True)
    with patch("db.supabase_client.supabase", mock_client):
        for mod in list(sys.modules.keys()):
            if mod.startswith(("routers", "main")):
                del sys.modules[mod]
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.post("/auth/login", json={
            "email": "no-es-un-email",
            "password": "password123",
        })
    assert response.status_code == 422


@pytest.mark.REQ_NF02
def test_logout_exitoso():
    """
    TC-021: POST /auth/logout retorna 204 sin contenido.

    Trazabilidad: REQ-NF02
    """
    mock_client = make_auth_mock(success=True)
    with patch("db.supabase_client.supabase", mock_client):
        for mod in list(sys.modules.keys()):
            if mod.startswith(("routers", "main")):
                del sys.modules[mod]
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        with patch("routers.auth._get_db", return_value=mock_client):
            response = client.post("/auth/logout")
    assert response.status_code == 204
