"""
Módulo: tests/test_repuestos.py
Responsabilidad: casos de prueba con BD real para el router de repuestos.
Trazabilidad: REQ-F01, REQ-F04
"""

import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _get_serie():
    """Genera numero de serie unico por timestamp para evitar conflictos."""
    return f"TEST-{int(time.time())}"


def _limpiar(serie):
    """Elimina repuesto de test y sus movimientos de la BD."""
    from db.supabase_client import supabase
    ids = supabase.table("repuestos").select("id").eq(
        "numero_serie", serie
    ).execute()
    for row in ids.data:
        supabase.table("movimientos").delete().eq(
            "repuesto_id", row["id"]
        ).execute()
    supabase.table("repuestos").delete().eq("numero_serie", serie).execute()


# ── REQ-F01 ──────────────────────────────────────────────────────────────────


@pytest.mark.REQ_F01
def test_crear_repuesto_exitoso():
    """
    TC-001: POST /repuestos con datos válidos retorna 201 y el repuesto creado.
    Trazabilidad: REQ-F01
    """
    serie = _get_serie()
    try:
        payload = {
            "nombre": "Repuesto Test",
            "categoria": "auto",
            "marca": "TestBrand",
            "numero_serie": serie,
            "precio": 1500.0,
            "stock_inicial": 10,
            "stock_minimo": 3,
        }
        response = client.post("/repuestos/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Repuesto Test"
        assert data["stock_actual"] == 10
        assert data["categoria"] == "auto"
    finally:
        _limpiar(serie)


@pytest.mark.REQ_F01
def test_crear_repuesto_precio_negativo():
    """
    TC-002: POST /repuestos con precio <= 0 retorna 422.
    Trazabilidad: REQ-F01
    """
    payload = {
        "nombre": "Repuesto Test",
        "categoria": "auto",
        "marca": "X",
        "numero_serie": _get_serie(),
        "precio": -100.0,
        "stock_inicial": 5,
    }
    response = client.post("/repuestos/", json=payload)
    assert response.status_code == 422


@pytest.mark.REQ_F01
def test_crear_repuesto_categoria_invalida():
    """
    TC-003: POST /repuestos con categoría inválida retorna 422.
    Trazabilidad: REQ-F01
    """
    payload = {
        "nombre": "Repuesto Test",
        "categoria": "barco",
        "marca": "X",
        "numero_serie": _get_serie(),
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
    response = client.get("/repuestos/999999")
    assert response.status_code == 404


# ── REQ-F04 ──────────────────────────────────────────────────────────────────


@pytest.mark.REQ_F04
def test_listar_repuestos_sin_filtro():
    """
    TC-005: GET /repuestos/ retorna lista completa de repuestos.
    Trazabilidad: REQ-F04
    """
    response = client.get("/repuestos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 12


@pytest.mark.REQ_F04
def test_listar_repuestos_filtro_categoria_auto():
    """
    TC-006: GET /repuestos/?categoria=auto retorna solo repuestos de autos.
    Trazabilidad: REQ-F04
    """
    response = client.get("/repuestos/?categoria=auto")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(r["categoria"] == "auto" for r in data)


@pytest.mark.REQ_F04
def test_listar_repuestos_filtro_categoria_moto():
    """
    TC-007: GET /repuestos/?categoria=moto retorna solo repuestos de motos.
    Trazabilidad: REQ-F04
    """
    response = client.get("/repuestos/?categoria=moto")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(r["categoria"] == "moto" for r in data)


@pytest.mark.REQ_F01
def test_actualizar_repuesto_exitoso():
    """
    TC-031: PATCH /repuestos/{id} actualiza precio y stock_minimo correctamente.

    Trazabilidad: REQ-F01
    """
    from db.supabase_client import supabase
    serie = _get_serie()
    try:
        rep = supabase.table("repuestos").insert({
            "nombre": "Repuesto Update Test",
            "categoria": "auto",
            "marca": "TestBrand",
            "numero_serie": serie,
            "precio": 1000.0,
            "stock_actual": 5,
            "stock_minimo": 2,
        }).execute()
        rep_id = rep.data[0]["id"]

        response = client.patch(f"/repuestos/{rep_id}", json={
            "precio": 2500.0,
            "stock_minimo": 4,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["precio"] == 2500.0
        assert data["stock_minimo"] == 4
        assert data["nombre"] == "Repuesto Update Test"
    finally:
        _limpiar(serie)


@pytest.mark.REQ_F01
def test_actualizar_repuesto_sin_datos():
    """
    TC-032: PATCH /repuestos/{id} sin campos retorna 400.

    Trazabilidad: REQ-F01
    """
    from db.supabase_client import supabase
    serie = _get_serie()
    try:
        rep = supabase.table("repuestos").insert({
            "nombre": "Repuesto Update Test 2",
            "categoria": "moto",
            "marca": "TestBrand",
            "numero_serie": serie,
            "precio": 500.0,
            "stock_actual": 3,
            "stock_minimo": 1,
        }).execute()
        rep_id = rep.data[0]["id"]

        response = client.patch(f"/repuestos/{rep_id}", json={})
        assert response.status_code == 400
    finally:
        _limpiar(serie)


@pytest.mark.REQ_F01
def test_actualizar_repuesto_precio_invalido():
    """
    TC-033: PATCH /repuestos/{id} con precio <= 0 retorna 422 (valor limite).

    Trazabilidad: REQ-F01
    """
    response = client.patch("/repuestos/1", json={"precio": -50.0})
    assert response.status_code == 422
