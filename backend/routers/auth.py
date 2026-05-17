"""
Módulo: routers/auth.py
Responsabilidad: login y logout del administrador via Supabase Auth.
El frontend nunca habla directo con Supabase — todo pasa por este endpoint.
Trazabilidad: REQ-NF02
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    """Schema de request para login de administrador."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema de response con el token JWT para el frontend."""

    access_token: str
    token_type: str = "bearer"
    user_email: str


def _get_db():
    """Importa el cliente Supabase de forma lazy para facilitar el testing."""
    from db.supabase_client import supabase
    return supabase


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    """
    Autentica al administrador contra Supabase Auth.
    Devuelve un JWT que el frontend usa en requests posteriores.

    Trazabilidad: REQ-NF02
    """
    db = _get_db()
    try:
        result = db.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password,
        })
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not result.session:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return LoginResponse(
        access_token=result.session.access_token,
        user_email=result.user.email,
    )


@router.post("/logout", status_code=204)
def logout():
    """
    Cierra la sesión del usuario en Supabase.

    Trazabilidad: REQ-NF02
    """
    db = _get_db()
    db.auth.sign_out()
