"""
Módulo: tests/test_stock.py
Responsabilidad: casos de prueba para entradas y salidas de stock.
Trazabilidad: REQ-F02, REQ-F03
"""

import pytest
from unittest.mock import MagicMock, patch

REPUESTO_BASE = {
    "id": 1,
    "nombre": "Pastilla de freno",
    "categoria": "auto",
    "marca": "ATE",
    "numero_serie": "AT-9999",
    "precio": 3200.0,
    "stock_actual": 8,
    "stock_minimo": 2,
}

MOVIMIENTO_ENTRADA = {
    "id": 1,
    "repuesto_id": 1,
    "tipo": "entrada",
    "cantidad": 5,
    "empleado": "Mirko",
    "fecha": "2026-05-20",
}

MOVIMIENTO_SALIDA = {
    "id": 2,
    "repuesto_id": 1,
    "tipo": "salida",
    "cantidad": 3,
    "empleado": "Celeste",
    "fecha": "2026-05-20",
}


def make_mock_stock(repuesto_data, movimiento_data):
    """Mock que devuelve el repuesto en el primer execute y el movimiento en el segundo."""
    result_repuesto = MagicMock()
    result_repuesto.data = [repuesto_data]
    result_movimiento = MagicMock()
    result_movimiento.data = [movimiento_data]
    result_update = MagicMock()
    result_update.data = [repuesto_data]

    query = MagicMock()
    query.eq.return_value = query
    query.select.return_value = query
    query.insert.return_value = query
    query.update.return_value = query
    query.execute.side_effect = [
        result_repuesto,
        result_update,
        result_movimiento,
    ]

    client = MagicMock()
    client.table.return_value = query
    return client


# ── REQ-F02 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F02
def test_registrar_entrada_exitosa():
    """
    TC-008: POST /stock/entrada con datos válidos retorna 201 y registra el movimiento.

    Trazabilidad: REQ-F02
    """
    mock_client = make_mock_stock(REPUESTO_BASE, MOVIMIENTO_ENTRADA)
    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 1,
            "cantidad": 5,
            "proveedor": "Distribuidora Sur",
            "empleado": "Mirko",
        }
        response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "entrada"


@pytest.mark.REQ_F02
def test_registrar_entrada_cantidad_cero():
    """
    TC-009: POST /stock/entrada con cantidad=0 retorna 422 (valor límite).

    Trazabilidad: REQ-F02
    """
    mock_client = make_mock_stock(REPUESTO_BASE, MOVIMIENTO_ENTRADA)
    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 1,
            "cantidad": 0,
            "proveedor": "Sur",
            "empleado": "Mirko",
        }
        response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 422


@pytest.mark.REQ_F02
def test_registrar_entrada_repuesto_inexistente():
    """
    TC-010: POST /stock/entrada con repuesto_id inexistente retorna 404.

    Trazabilidad: REQ-F02
    """
    result_vacio = MagicMock()
    result_vacio.data = []
    query = MagicMock()
    query.eq.return_value = query
    query.select.return_value = query
    query.execute.return_value = result_vacio
    mock_client = MagicMock()
    mock_client.table.return_value = query

    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 9999,
            "cantidad": 5,
            "proveedor": "Sur",
            "empleado": "Mirko",
        }
        response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 404


# ── REQ-F03 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F03
def test_registrar_salida_exitosa():
    """
    TC-011: POST /stock/salida con stock suficiente retorna 201.

    Trazabilidad: REQ-F03
    """
    mock_client = make_mock_stock(REPUESTO_BASE, MOVIMIENTO_SALIDA)
    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 1,
            "cantidad": 3,
            "empleado": "Celeste",
            "finalidad": "venta",
        }
        response = client.post("/stock/salida", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "salida"


@pytest.mark.REQ_F03
def test_registrar_salida_stock_insuficiente():
    """
    TC-012: POST /stock/salida con cantidad mayor al stock retorna 400.
    Verifica que el sistema impide stock negativo.

    Trazabilidad: REQ-F03
    """
    repuesto_poco_stock = {**REPUESTO_BASE, "stock_actual": 2}
    result = MagicMock()
    result.data = [repuesto_poco_stock]
    query = MagicMock()
    query.eq.return_value = query
    query.select.return_value = query
    query.execute.return_value = result
    mock_client = MagicMock()
    mock_client.table.return_value = query

    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 1,
            "cantidad": 10,
            "empleado": "Daniel",
            "finalidad": "uso interno",
        }
        response = client.post("/stock/salida", json=payload)
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["detail"]


@pytest.mark.REQ_F03
def test_registrar_salida_stock_exacto():
    """
    TC-013: POST /stock/salida con cantidad == stock_actual (valor límite) retorna 201.

    Trazabilidad: REQ-F03
    """
    repuesto_stock_exacto = {**REPUESTO_BASE, "stock_actual": 5}
    movimiento = {**MOVIMIENTO_SALIDA, "cantidad": 5}
    mock_client = make_mock_stock(repuesto_stock_exacto, movimiento)

    with patch("routers.stock._get_db", return_value=mock_client):
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        payload = {
            "repuesto_id": 1,
            "cantidad": 5,
            "empleado": "Daniel",
            "finalidad": "venta",
        }
        response = client.post("/stock/salida", json=payload)
    assert response.status_code == 201
