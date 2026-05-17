"""
Módulo: routers/stock.py
Responsabilidad: endpoints para registrar entradas y salidas de stock.
Trazabilidad: REQ-F02, REQ-F03
"""

from fastapi import APIRouter, HTTPException
from datetime import date
from schemas.movimiento import (
    EntradaStockCreate,
    SalidaStockCreate,
    MovimientoResponse,
)

router = APIRouter(prefix="/stock", tags=["Stock"])


def _get_db():
    """Importa el cliente Supabase de forma lazy para facilitar el testing."""
    from db.supabase_client import supabase
    return supabase


def _obtener_repuesto(db, repuesto_id: int) -> dict:
    """
    Obtiene un repuesto por ID. Lanza 404 si no existe.

    Trazabilidad: REQ-F02, REQ-F03
    """
    result = db.table("repuestos").select("*").eq("id", repuesto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return result.data[0]


@router.post("/entrada", response_model=MovimientoResponse, status_code=201)
def registrar_entrada(entrada: EntradaStockCreate):
    """
    Registra una entrada de stock (reposición) para un repuesto.
    Actualiza el stock_actual sumando la cantidad recibida.

    Trazabilidad: REQ-F02
    """
    db = _get_db()
    repuesto = _obtener_repuesto(db, entrada.repuesto_id)

    nuevo_stock = repuesto["stock_actual"] + entrada.cantidad
    db.table("repuestos").update(
        {"stock_actual": nuevo_stock}
    ).eq("id", entrada.repuesto_id).execute()

    movimiento = {
        "repuesto_id": entrada.repuesto_id,
        "tipo": "entrada",
        "cantidad": entrada.cantidad,
        "proveedor": entrada.proveedor,
        "empleado": entrada.empleado,
        "fecha": str(entrada.fecha or date.today()),
    }
    result = db.table("movimientos").insert(movimiento).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al registrar la entrada")
    return result.data[0]


@router.post("/salida", response_model=MovimientoResponse, status_code=201)
def registrar_salida(salida: SalidaStockCreate):
    """
    Registra una salida de stock (venta o uso) para un repuesto.
    Impide la operación si el stock resultante sería negativo.

    Trazabilidad: REQ-F03
    """
    db = _get_db()
    repuesto = _obtener_repuesto(db, salida.repuesto_id)

    stock_resultante = repuesto["stock_actual"] - salida.cantidad
    if stock_resultante < 0:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Stock insuficiente. Stock actual: {repuesto['stock_actual']}, "
                f"cantidad solicitada: {salida.cantidad}"
            ),
        )

    db.table("repuestos").update(
        {"stock_actual": stock_resultante}
    ).eq("id", salida.repuesto_id).execute()

    movimiento = {
        "repuesto_id": salida.repuesto_id,
        "tipo": "salida",
        "cantidad": salida.cantidad,
        "empleado": salida.empleado,
        "finalidad": salida.finalidad,
        "fecha": str(date.today()),
    }
    result = db.table("movimientos").insert(movimiento).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al registrar la salida")
    return result.data[0]
