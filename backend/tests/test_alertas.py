"""
Módulo: tests/test_alertas.py
Responsabilidad: casos de prueba para stock crítico y healthcheck.
Trazabilidad: REQ-F05, REQ-NF01
"""

import pytest
from unittest.mock import MagicMock, patch

REPUESTO_CRITICO = {
    "id": 1,
    "nombre": "Bujia NGK",
    "categoria": "moto",
    "marca": "NGK",
    "numero_serie": "NGK-001",
    "precio": 800.0,
    "stock_actual": 2,
    "stock_minimo": 5,
}

REPUESTO_OK = {
    "id": 2,
    "nombre": "Aceite motor",
    "categoria": "auto",
    "marca": "Shell",
    "numero_serie": "SH-002",
    "precio": 4500.0,
    "stock_actual": 20,
    "stock_minimo": 3,
}

REPUESTO_EN_LIMITE = {
    "id": 3,
    "nombre": "Filtro aire",
    "categoria": "camioneta",
    "marca": "Mann",
    "numero_serie": "MN-003",
    "precio": 1200.0,
    "stock_actual": 5,
    "stock_minimo": 5,
}


def make_mock(data):
    result = MagicMock()
    result.data = data
    query = MagicMock()
    query.select.return_value = query
    query.execute.return_value = result
    client = MagicMock()
    client.table.return_value = query
    return client


# ── REQ-F05 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F05
def test_stock_critico_retorna_solo_criticos():
    """
    TC-014: GET /alertas/stock-critico retorna solo repuestos con
    stock_actual <= stock_minimo.

    Trazabilidad: REQ-F05
    """
    mock_client = make_mock([REPUESTO_CRITICO, REPUESTO_OK])
    with patch("routers.alertas._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Bujia NGK"


@pytest.mark.REQ_F05
def test_stock_critico_incluye_limite_exacto():
    """
    TC-015: GET /alertas/stock-critico incluye repuestos con
    stock_actual == stock_minimo (valor límite).

    Trazabilidad: REQ-F05
    """
    mock_client = make_mock([REPUESTO_EN_LIMITE, REPUESTO_OK])
    with patch("routers.alertas._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    nombres = [r["nombre"] for r in response.json()]
    assert "Filtro aire" in nombres


@pytest.mark.REQ_F05
def test_stock_critico_vacio_cuando_todo_ok():
    """
    TC-016: GET /alertas/stock-critico retorna lista vacía si todos
    los repuestos tienen stock suficiente.

    Trazabilidad: REQ-F05
    """
    mock_client = make_mock([REPUESTO_OK])
    with patch("routers.alertas._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    assert response.json() == []


# ── REQ-NF01 ─────────────────────────────────────────────────────────────────

@pytest.mark.REQ_NF01
def test_healthcheck():
    """
    TC-017: GET /health retorna status ok. Verifica que la app responde.

    Trazabilidad: REQ-NF01
    """
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
