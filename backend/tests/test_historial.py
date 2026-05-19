"""
Módulo: tests/test_historial.py
Responsabilidad: casos de prueba con BD real para el router de historial.
Trazabilidad: REQ-F02, REQ-F03
"""

import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def repuesto_con_movimientos():
    """
    Crea un repuesto de prueba con 2 movimientos (1 entrada, 1 salida).
    Usa milliseconds en el timestamp para evitar conflictos entre tests.
    Lo limpia al terminar.

    Trazabilidad: REQ-F02, REQ-F03
    """
    from db.supabase_client import supabase

    serie = f"TEST-H-{int(time.time() * 1000)}"

    rep = supabase.table("repuestos").insert({
        "nombre": "Repuesto Historial Test",
        "categoria": "auto",
        "marca": "TestBrand",
        "numero_serie": serie,
        "precio": 1000.0,
        "stock_actual": 10,
        "stock_minimo": 3,
    }).execute()
    rep_id = rep.data[0]["id"]

    supabase.table("movimientos").insert({
        "repuesto_id": rep_id,
        "tipo": "entrada",
        "cantidad": 5,
        "empleado": "Mirko Bubica",
        "proveedor": "Proveedor Test",
        "fecha": "2026-05-01",
    }).execute()

    supabase.table("movimientos").insert({
        "repuesto_id": rep_id,
        "tipo": "salida",
        "cantidad": 2,
        "empleado": "Celeste Nuñez",
        "finalidad": "venta test",
        "fecha": "2026-05-02",
    }).execute()

    yield {"repuesto_id": rep_id, "serie": serie}

    supabase.table("movimientos").delete().eq("repuesto_id", rep_id).execute()
    supabase.table("repuestos").delete().eq("id", rep_id).execute()


# ── REQ-F02 / REQ-F03 ────────────────────────────────────────────────────────


@pytest.mark.REQ_F02
@pytest.mark.REQ_F03
def test_historial_retorna_lista(repuesto_con_movimientos):
    """
    TC-022: GET /historial/ retorna lista con movimientos del repuesto de prueba.
    Verifica que el endpoint incluye datos del repuesto en cada movimiento.

    Trazabilidad: REQ-F02, REQ-F03
    """
    response = client.get("/historial/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    primer = data[0]
    assert "repuesto_nombre" in primer
    assert "repuesto_categoria" in primer
    assert "repuesto_marca" in primer
    assert "repuesto_numero_serie" in primer
    assert "tipo" in primer
    assert "cantidad" in primer
    assert "empleado" in primer
    assert "fecha" in primer


@pytest.mark.REQ_F02
def test_historial_filtro_tipo_entrada(repuesto_con_movimientos):
    """
    TC-023: GET /historial/?tipo=entrada retorna solo movimientos de entrada.

    Trazabilidad: REQ-F02
    """
    response = client.get("/historial/?tipo=entrada")
    assert response.status_code == 200
    data = response.json()
    assert all(m["tipo"] == "entrada" for m in data)


@pytest.mark.REQ_F03
def test_historial_filtro_tipo_salida(repuesto_con_movimientos):
    """
    TC-024: GET /historial/?tipo=salida retorna solo movimientos de salida.

    Trazabilidad: REQ-F03
    """
    response = client.get("/historial/?tipo=salida")
    assert response.status_code == 200
    data = response.json()
    assert all(m["tipo"] == "salida" for m in data)


@pytest.mark.REQ_F02
@pytest.mark.REQ_F03
def test_historial_filtro_repuesto(repuesto_con_movimientos):
    """
    TC-025: GET /historial/?repuesto_id=X retorna solo movimientos de ese repuesto.

    Trazabilidad: REQ-F02, REQ-F03
    """
    rep_id = repuesto_con_movimientos["repuesto_id"]
    response = client.get(f"/historial/?repuesto_id={rep_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(m["repuesto_id"] == rep_id for m in data)


@pytest.mark.REQ_F02
def test_historial_filtro_empleado(repuesto_con_movimientos):
    """
    TC-026: GET /historial/?empleado=Mirko retorna movimientos de ese empleado.

    Trazabilidad: REQ-F02
    """
    response = client.get("/historial/?empleado=Mirko")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("Mirko" in m["empleado"] for m in data)


@pytest.mark.REQ_F02
@pytest.mark.REQ_F03
def test_historial_por_repuesto(repuesto_con_movimientos):
    """
    TC-027: GET /historial/{repuesto_id} retorna historial completo del repuesto
    con datos del repuesto incluidos en cada movimiento.

    Trazabilidad: REQ-F02, REQ-F03
    """
    rep_id = repuesto_con_movimientos["repuesto_id"]
    serie = repuesto_con_movimientos["serie"]
    response = client.get(f"/historial/{rep_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    tipos = {m["tipo"] for m in data}
    assert "entrada" in tipos
    assert "salida" in tipos
    assert data[0]["repuesto_nombre"] == "Repuesto Historial Test"
    assert data[0]["repuesto_numero_serie"] == serie


@pytest.mark.REQ_F02
@pytest.mark.REQ_F03
def test_historial_repuesto_no_encontrado():
    """
    TC-028: GET /historial/{id} con ID inexistente retorna 404.

    Trazabilidad: REQ-F02, REQ-F03
    """
    response = client.get("/historial/999999")
    assert response.status_code == 404


@pytest.mark.REQ_F02
def test_historial_datos_entrada(repuesto_con_movimientos):
    """
    TC-029: Los movimientos de entrada incluyen proveedor y finalidad es None.

    Trazabilidad: REQ-F02
    """
    rep_id = repuesto_con_movimientos["repuesto_id"]
    response = client.get(f"/historial/{rep_id}")
    assert response.status_code == 200
    entradas = [m for m in response.json() if m["tipo"] == "entrada"]
    assert len(entradas) == 1
    assert entradas[0]["proveedor"] == "Proveedor Test"
    assert entradas[0]["finalidad"] is None


@pytest.mark.REQ_F03
def test_historial_datos_salida(repuesto_con_movimientos):
    """
    TC-030: Los movimientos de salida incluyen finalidad y proveedor es None.

    Trazabilidad: REQ-F03
    """
    rep_id = repuesto_con_movimientos["repuesto_id"]
    response = client.get(f"/historial/{rep_id}")
    assert response.status_code == 200
    salidas = [m for m in response.json() if m["tipo"] == "salida"]
    assert len(salidas) == 1
    assert salidas[0]["finalidad"] == "venta test"
    assert salidas[0]["proveedor"] is None
