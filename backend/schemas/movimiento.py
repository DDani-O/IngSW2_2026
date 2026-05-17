"""
Módulo: schemas/movimiento.py
Responsabilidad: validación de entradas y salidas de stock.
Trazabilidad: REQ-F02, REQ-F03
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date


class TipoMovimiento(str, Enum):
    """Tipo de movimiento de stock."""

    entrada = "entrada"
    salida = "salida"


class EntradaStockCreate(BaseModel):
    """
    Schema para registrar una entrada de stock (reposición).

    Trazabilidad: REQ-F02
    """

    repuesto_id: int
    cantidad: int = Field(..., gt=0)
    proveedor: str = Field(..., min_length=2, max_length=100)
    empleado: str = Field(..., min_length=2, max_length=80)
    fecha: Optional[date] = None


class SalidaStockCreate(BaseModel):
    """
    Schema para registrar una salida de stock (venta o uso).

    Trazabilidad: REQ-F03
    """

    repuesto_id: int
    cantidad: int = Field(..., gt=0)
    empleado: str = Field(..., min_length=2, max_length=80)
    finalidad: str = Field(..., min_length=2, max_length=100)


class MovimientoResponse(BaseModel):
    """
    Schema de respuesta para un movimiento de stock.

    Trazabilidad: REQ-F02, REQ-F03
    """

    id: int
    repuesto_id: int
    tipo: TipoMovimiento
    cantidad: int
    empleado: str
    fecha: date

    class Config:
        from_attributes = True
