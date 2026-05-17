"""
Módulo: tests/test_repuestos.py
Responsabilidad: casos de prueba para el router de repuestos.
Trazabilidad: REQ-F01, REQ-F04
"""

import pytest
from unittest.mock import MagicMock, patch

REPUESTO_BASE = {
    "id": 1,
    "nombre": "Filtro de aceite",
    "categoria": "auto",
    "marca": "Bosch",
    "numero_serie": "BO-1234",
    "precio": 1500.0,
    "stock_actual": 10,
    "stock_minimo": 3,
}


def make_mock(data):
    """Construye un mock de Supabase que retorna data."""
    result = MagicMock()
    result.data = data
    query = MagicMock()
    query.execute.return_value = result
    query.eq.return_value = query
    query.ilike.return_value = query
    query.select.return_value = query
    query.insert.return_value = query
    query.update.return_value = query
    client = MagicMock()
    client.table.return_value = query
    return client


# ── REQ-F01 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F01
def test_crear_repuesto_exitoso():
    """
    TC-001: POST /repuestos con datos válidos retorna 201 y el repuesto creado.

    Trazabilidad: REQ-F01
    """
    mock_client = make_mock([REPUESTO_BASE])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "nombre": "Filtro de aceite",
            "categoria": "auto",
            "marca": "Bosch",
            "numero_serie": "BO-1234",
            "precio": 1500.0,
            "stock_inicial": 10,
            "stock_minimo": 3,
        }
        response = client.post("/repuestos/", json=payload)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Filtro de aceite"


@pytest.mark.REQ_F01
def test_crear_repuesto_precio_negativo():
    """
    TC-002: POST /repuestos con precio <= 0 retorna 422 (validación Pydantic).

    Trazabilidad: REQ-F01
    """
    mock_client = make_mock([])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "nombre": "Filtro",
            "categoria": "auto",
            "marca": "X",
            "numero_serie": "X-1",
            "precio": -100.0,
            "stock_inicial": 5,
        }
        response = client.post("/repuestos/", json=payload)
    assert response.status_code == 422


@pytest.mark.REQ_F01
def test_crear_repuesto_categoria_invalida():
    """
    TC-003: POST /repuestos con categoría fuera del enum retorna 422.

    Trazabilidad: REQ-F01
    """
    mock_client = make_mock([])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "nombre": "Filtro",
            "categoria": "barco",
            "marca": "X",
            "numero_serie": "X-1",
            "precio": 100.0,
            "stock_inicial": 5,
        }
        response = client.post("/repuestos/", json=payload)
    assert response.status_code == 422


@pytest.mark.REQ_F01
def test_obtener_repuesto_no_encontrado():
    """
    TC-004: GET /repuestos/{id} con ID inexistente retorna 404.

    Trazabilidad: REQ-F01
    """
    mock_client = make_mock([])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/repuestos/999")
    assert response.status_code == 404


# ── REQ-F04 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F04
def test_listar_repuestos_sin_filtro():
    """
    TC-005: GET /repuestos/ retorna lista completa de repuestos.

    Trazabilidad: REQ-F04
    """
    mock_client = make_mock([REPUESTO_BASE])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/repuestos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.REQ_F04
def test_listar_repuestos_filtro_categoria():
    """
    TC-006: GET /repuestos/?categoria=auto filtra por categoría correctamente.

    Trazabilidad: REQ-F04
    """
    mock_client = make_mock([REPUESTO_BASE])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/repuestos/?categoria=auto")
    assert response.status_code == 200
    assert response.json()[0]["categoria"] == "auto"


@pytest.mark.REQ_F04
def test_listar_repuestos_categoria_invalida():
    """
    TC-007: GET /repuestos/?categoria=invalida retorna 422.

    Trazabilidad: REQ-F04
    """
    mock_client = make_mock([])
    with patch("routers.repuestos._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/repuestos/?categoria=barco")
    assert response.status_code == 422
