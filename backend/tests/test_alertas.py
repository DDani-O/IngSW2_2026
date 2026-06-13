"""
Módulo: tests/test_alertas.py
Responsabilidad: casos de prueba con BD real para stock crítico y healthcheck.
Trazabilidad: REQ-F05, REQ-NF01
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ── REQ-F05 ──────────────────────────────────────────────────────────────────


@pytest.mark.REQ_F05
def test_stock_critico_retorna_solo_criticos():
    """
    TC-014: GET /alertas/stock-critico retorna solo repuestos con stock <= minimo.
    Trazabilidad: REQ-F05
    """
    response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    data = response.json()
    # Todos los retornados deben tener stock_actual <= stock_minimo
    assert isinstance(data, list)
    for r in data:
        assert r["stock_actual"] <= r["stock_minimo"]


@pytest.mark.REQ_F05
def test_stock_critico_incluye_limite_exacto():
    """
    TC-015: Repuesto con stock_actual == stock_minimo debe aparecer en stock crítico.
    Trazabilidad: REQ-F05
    """
    # Disco de freno trasero: stock_actual=5, stock_minimo=5 (exactamente igual)
    response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    nombres = [r["nombre"] for r in response.json()]
    assert "Disco de freno trasero" in nombres


@pytest.mark.REQ_F05
def test_stock_critico_no_incluye_stock_suficiente():
    """
    TC-016: Repuesto con stock_actual > stock_minimo NO debe aparecer en stock crítico.
    Trazabilidad: REQ-F05
    """
    response = client.get("/alertas/stock-critico")
    assert response.status_code == 200
    # Filtro de aceite: stock=12, minimo=5 — no debe estar
    nombres = [r["nombre"] for r in response.json()]
    assert "Filtro de aceite" not in nombres


# ── REQ-NF01 ─────────────────────────────────────────────────────────────────

@pytest.mark.REQ_NF01
def test_healthcheck():
    """
    TC-017: GET /health retorna 200 con status ok.
    Trazabilidad: REQ-NF01
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.REQ_NF01
def test_consulta_repuestos_con_500_o_mas_responde_bajo_2_segundos():
    """
    TC-NF01-001: GET /repuestos/ responde en menos de 2 segundos
    con al menos 500 repuestos cargados en la base de datos.

    Trazabilidad: REQ-NF01
    """
    import time

    start = time.perf_counter()
    response = client.get("/repuestos/")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 500, (
        f"Se requieren >= 500 repuestos para validar REQ-NF01, "
        f"hay {len(data)}"
    )
    assert elapsed < 2.0, (
        f"La consulta tardo {elapsed:.4f}s, supera el umbral de 2s de REQ-NF01"
    )
