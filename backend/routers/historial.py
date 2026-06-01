"""
Módulo: routers/historial.py
Responsabilidad: endpoints para consultar el historial de movimientos de stock,
con datos del repuesto asociado incluidos en la respuesta.
Trazabilidad: REQ-F02, REQ-F03
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/historial", tags=["Historial"])


class MovimientoDetalle(BaseModel):
    """
    Schema de respuesta para un movimiento con datos del repuesto incluidos.

    Trazabilidad: REQ-F02, REQ-F03
    """

    id: int
    tipo: str
    cantidad: int
    empleado: str
    proveedor: Optional[str] = None
    finalidad: Optional[str] = None
    fecha: str
    created_at: str
    repuesto_id: int
    repuesto_nombre: str
    repuesto_categoria: str
    repuesto_marca: str
    repuesto_numero_serie: str
    stock_actual: int


def _get_db():
    """Importa el cliente Supabase de forma lazy para facilitar el testing."""
    from db.supabase_client import supabase
    return supabase


def _aplicar_filtros(query, tipo, repuesto_id, empleado, fecha_desde, fecha_hasta):
    """
    Aplica filtros opcionales a una query de movimientos.

    Trazabilidad: REQ-F02, REQ-F03
    """
    if tipo:
        query = query.eq("tipo", tipo)
    if repuesto_id:
        query = query.eq("repuesto_id", repuesto_id)
    if empleado:
        query = query.ilike("empleado", f"%{empleado}%")
    if fecha_desde:
        query = query.gte("fecha", str(fecha_desde))
    if fecha_hasta:
        query = query.lte("fecha", str(fecha_hasta))
    return query


def _construir_detalle(m: dict, rep: dict) -> MovimientoDetalle:
    """
    Construye un MovimientoDetalle combinando un movimiento y su repuesto.

    Trazabilidad: REQ-F02, REQ-F03
    """
    return MovimientoDetalle(
        id=m["id"],
        tipo=m["tipo"],
        cantidad=m["cantidad"],
        empleado=m["empleado"],
        proveedor=m.get("proveedor"),
        finalidad=m.get("finalidad"),
        fecha=m["fecha"],
        created_at=m["created_at"],
        repuesto_id=rep["id"],
        repuesto_nombre=rep["nombre"],
        repuesto_categoria=rep["categoria"],
        repuesto_marca=rep["marca"],
        repuesto_numero_serie=rep["numero_serie"],
        stock_actual=rep["stock_actual"],
    )


def _obtener_repuestos_map(db, movimientos: list) -> dict:
    """
    Obtiene un mapa id->repuesto para los repuestos de una lista de movimientos.

    Trazabilidad: REQ-F02, REQ-F03
    """
    ids = list({m["repuesto_id"] for m in movimientos})
    resultado = db.table("repuestos").select(
        "id, nombre, categoria, marca, numero_serie, stock_actual"
    ).in_("id", ids).execute()
    return {r["id"]: r for r in resultado.data}


@router.get("/", response_model=List[MovimientoDetalle])
def listar_historial(
    tipo: Optional[str] = Query(default=None, description="entrada o salida"),
    repuesto_id: Optional[int] = Query(default=None),
    empleado: Optional[str] = Query(default=None),
    fecha_desde: Optional[date] = Query(default=None),
    fecha_hasta: Optional[date] = Query(default=None),
    limite: int = Query(default=50, le=200),
):
    """
    Lista el historial completo de movimientos con datos del repuesto incluidos.
    Soporta filtros por tipo, repuesto, empleado y rango de fechas.

    Trazabilidad: REQ-F02, REQ-F03
    """
    db = _get_db()
    query = db.table("movimientos").select("*").order(
        "created_at", desc=True
    ).limit(limite)
    query = _aplicar_filtros(query, tipo, repuesto_id, empleado, fecha_desde, fecha_hasta)
    movimientos = query.execute().data

    if not movimientos:
        return []

    repuestos_map = _obtener_repuestos_map(db, movimientos)
    return [
        _construir_detalle(m, repuestos_map[m["repuesto_id"]])
        for m in movimientos
        if m["repuesto_id"] in repuestos_map
    ]


@router.get("/{repuesto_id}", response_model=List[MovimientoDetalle])
def historial_por_repuesto(repuesto_id: int):
    """
    Lista todos los movimientos de un repuesto específico, ordenados por fecha desc.

    Trazabilidad: REQ-F02, REQ-F03
    """
    db = _get_db()
    repuesto = db.table("repuestos").select(
        "id, nombre, categoria, marca, numero_serie, stock_actual"
    ).eq("id", repuesto_id).execute()

    if not repuesto.data:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")

    rep = repuesto.data[0]
    movimientos = db.table("movimientos").select("*").eq(
        "repuesto_id", repuesto_id
    ).order("created_at", desc=True).execute().data

    return [_construir_detalle(m, rep) for m in movimientos]
