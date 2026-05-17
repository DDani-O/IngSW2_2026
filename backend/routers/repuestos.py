"""
Módulo: routers/repuestos.py
Responsabilidad: endpoints CRUD para gestión de repuestos.
Trazabilidad: REQ-F01, REQ-F04
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from schemas.repuesto import RepuestoCreate, RepuestoResponse, RepuestoUpdate, Categoria

router = APIRouter(prefix="/repuestos", tags=["Repuestos"])


def _get_db():
    """Importa el cliente Supabase de forma lazy para facilitar el testing."""
    from db.supabase_client import supabase
    return supabase


@router.post("/", response_model=RepuestoResponse, status_code=201)
def crear_repuesto(repuesto: RepuestoCreate):
    """
    Registra un nuevo repuesto en el sistema.

    Trazabilidad: REQ-F01
    """
    db = _get_db()
    data = repuesto.model_dump()
    data["stock_actual"] = data.pop("stock_inicial")

    result = db.table("repuestos").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al crear el repuesto")
    return result.data[0]


@router.get("/", response_model=List[RepuestoResponse])
def listar_repuestos(
    categoria: Optional[Categoria] = Query(default=None),
    nombre: Optional[str] = Query(default=None),
):
    """
    Lista todos los repuestos con filtros opcionales por categoría y nombre.

    Trazabilidad: REQ-F04
    """
    db = _get_db()
    query = db.table("repuestos").select("*")

    if categoria:
        query = query.eq("categoria", categoria.value)
    if nombre:
        query = query.ilike("nombre", f"%{nombre}%")

    result = query.execute()
    return result.data


@router.get("/{repuesto_id}", response_model=RepuestoResponse)
def obtener_repuesto(repuesto_id: int):
    """
    Obtiene un repuesto por su ID.

    Trazabilidad: REQ-F01, REQ-F04
    """
    db = _get_db()
    result = db.table("repuestos").select("*").eq("id", repuesto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return result.data[0]


@router.patch("/{repuesto_id}", response_model=RepuestoResponse)
def actualizar_repuesto(repuesto_id: int, datos: RepuestoUpdate):
    """
    Actualiza campos opcionales de un repuesto (nombre, precio, stock_minimo).

    Trazabilidad: REQ-F01
    """
    db = _get_db()
    payload = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    result = db.table("repuestos").update(payload).eq("id", repuesto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return result.data[0]
