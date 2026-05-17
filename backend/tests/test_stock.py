"""
Módulo: tests/test_stock.py
Responsabilidad: casos de prueba con BD real para entradas y salidas de stock.
Trazabilidad: REQ-F02, REQ-F03
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_SERIE_STOCK = "TEST-STK-9992"


@pytest.fixture
def repuesto_test():
    """Crea un repuesto de prueba con stock conocido y lo elimina al final."""
    from db.supabase_client import supabase
    # Upsert por numero_serie para evitar conflictos entre tests
    result = supabase.table("repuestos").upsert({
        "nombre": "Repuesto Stock Test",
        "categoria": "moto",
        "marca": "TestBrand",
        "numero_serie": TEST_SERIE_STOCK,
        "precio": 999.0,
        "stock_actual": 10,
        "stock_minimo": 3,
    }, on_conflict="numero_serie").execute()
    repuesto_id = result.data[0]["id"]
    # Resetear stock a 10 por si un test anterior lo modificó
    supabase.table("repuestos").update({"stock_actual": 10}).eq("id", repuesto_id).execute()
    yield repuesto_id
    supabase.table("movimientos").delete().eq("repuesto_id", repuesto_id).execute()
    supabase.table("repuestos").delete().eq("id", repuesto_id).execute()


# ── REQ-F02 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F02
def test_registrar_entrada_exitosa(repuesto_test):
    """
    TC-008: POST /stock/entrada con datos válidos retorna 201 y actualiza stock.
    Trazabilidad: REQ-F02
    """
    from db.supabase_client import supabase
    payload = {
        "repuesto_id": repuesto_test,
        "cantidad": 5,
        "proveedor": "Distribuidora Test",
        "empleado": "Mirko Bubica",
    }
    response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "entrada"
    # Verificar que el stock se actualizó en BD
    r = supabase.table("repuestos").select("stock_actual").eq("id", repuesto_test).execute()
    assert r.data[0]["stock_actual"] == 15  # 10 + 5


@pytest.mark.REQ_F02
def test_registrar_entrada_cantidad_cero(repuesto_test):
    """
    TC-009: POST /stock/entrada con cantidad=0 retorna 422 (valor límite).
    Trazabilidad: REQ-F02
    """
    payload = {
        "repuesto_id": repuesto_test,
        "cantidad": 0,
        "proveedor": "Sur",
        "empleado": "Mirko Bubica",
    }
    response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 422


@pytest.mark.REQ_F02
def test_registrar_entrada_repuesto_inexistente():
    """
    TC-010: POST /stock/entrada con repuesto_id inexistente retorna 404.
    Trazabilidad: REQ-F02
    """
    payload = {
        "repuesto_id": 999999,
        "cantidad": 5,
        "proveedor": "Sur",
        "empleado": "Mirko Bubica",
    }
    response = client.post("/stock/entrada", json=payload)
    assert response.status_code == 404


# ── REQ-F03 ──────────────────────────────────────────────────────────────────

@pytest.mark.REQ_F03
def test_registrar_salida_exitosa(repuesto_test):
    """
    TC-011: POST /stock/salida con stock suficiente retorna 201 y descuenta stock.
    Trazabilidad: REQ-F03
    """
    from db.supabase_client import supabase
    payload = {
        "repuesto_id": repuesto_test,
        "cantidad": 3,
        "empleado": "Celeste Nuñez",
        "finalidad": "venta",
    }
    response = client.post("/stock/salida", json=payload)
    assert response.status_code == 201
    assert response.json()["tipo"] == "salida"
    # Verificar que el stock se descontó en BD
    r = supabase.table("repuestos").select("stock_actual").eq("id", repuesto_test).execute()
    assert r.data[0]["stock_actual"] == 7  # 10 - 3


@pytest.mark.REQ_F03
def test_registrar_salida_stock_insuficiente(repuesto_test):
    """
    TC-012: POST /stock/salida con cantidad > stock retorna 400. Impide stock negativo.
    Trazabilidad: REQ-F03
    """
    payload = {
        "repuesto_id": repuesto_test,
        "cantidad": 100,
        "empleado": "Daniel Olguin",
        "finalidad": "uso interno",
    }
    response = client.post("/stock/salida", json=payload)
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["detail"]


@pytest.mark.REQ_F03
def test_registrar_salida_stock_exacto(repuesto_test):
    """
    TC-013: POST /stock/salida con cantidad == stock_actual retorna 201 (valor límite).
    Trazabilidad: REQ-F03
    """
    from db.supabase_client import supabase
    payload = {
        "repuesto_id": repuesto_test,
        "cantidad": 10,
        "empleado": "Daniel Olguin",
        "finalidad": "venta total",
    }
    response = client.post("/stock/salida", json=payload)
    assert response.status_code == 201
    # Stock debe quedar en 0
    r = supabase.table("repuestos").select("stock_actual").eq("id", repuesto_test).execute()
    assert r.data[0]["stock_actual"] == 0
