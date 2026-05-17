"""
Módulo: routers/alertas.py
Responsabilidad: endpoint para listar repuestos en stock crítico.
Trazabilidad: REQ-F05
"""

from fastapi import APIRouter
from typing import List
from schemas.repuesto import RepuestoResponse

router = APIRouter(prefix="/alertas", tags=["Alertas"])


def _get_db():
    """Importa el cliente Supabase de forma lazy para facilitar el testing."""
    from db.supabase_client import get_client as supabase
    return supabase()


@router.get("/stock-critico", response_model=List[RepuestoResponse])
def listar_stock_critico():
    """
    Lista todos los repuestos cuyo stock_actual sea menor o igual
    al stock_minimo configurado.

    Trazabilidad: REQ-F05
    """
    db = _get_db()
    result = db.table("repuestos").select("*").execute()

    criticos = [
        r for r in result.data
        if r["stock_actual"] <= r["stock_minimo"]
    ]
    return criticos
