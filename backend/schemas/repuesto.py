"""
Módulo: schemas/repuesto.py
Responsabilidad: validación y serialización de datos de repuestos.
Trazabilidad: REQ-F01
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Categoria(str, Enum):
    """Categorías válidas de repuestos."""

    auto = "auto"
    moto = "moto"
    camioneta = "camioneta"


class RepuestoCreate(BaseModel):
    """
    Schema para crear un nuevo repuesto.

    Trazabilidad: REQ-F01
    """

    nombre: str = Field(..., min_length=2, max_length=100)
    categoria: Categoria
    marca: str = Field(..., min_length=1, max_length=80)
    numero_serie: str = Field(..., min_length=1, max_length=60)
    precio: float = Field(..., gt=0)
    stock_inicial: int = Field(..., ge=0)
    stock_minimo: int = Field(default=5, ge=0)


class RepuestoResponse(BaseModel):
    """
    Schema de respuesta para un repuesto.

    Trazabilidad: REQ-F01, REQ-F04
    """

    id: int
    nombre: str
    categoria: Categoria
    marca: str
    numero_serie: str
    precio: float
    stock_actual: int
    stock_minimo: int

    class Config:
        from_attributes = True


class RepuestoUpdate(BaseModel):
    """
    Schema para actualizar campos opcionales de un repuesto.

    Trazabilidad: REQ-F01
    """

    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    categoria: Optional[Categoria] = None
    marca: Optional[str] = Field(default=None, min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, min_length=1, max_length=60)
    precio: Optional[float] = Field(default=None, gt=0)
    stock_minimo: Optional[int] = Field(default=None, ge=0)
