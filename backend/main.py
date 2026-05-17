"""
Módulo: main.py
Responsabilidad: punto de entrada de la aplicación FastAPI.
Configura CORS, registra routers y expone el healthcheck.
Trazabilidad: REQ-NF01, REQ-NF02
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import repuestos, stock, alertas, auth

load_dotenv()

app = FastAPI(
    title="AutoBhan Autopartes API",
    description="Sistema de gestión de inventario de repuestos de automotores.",
    version="1.0.0",
)

# CORS — permite requests desde el frontend React
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(repuestos.router)
app.include_router(stock.router)
app.include_router(alertas.router)


@app.get("/health", tags=["Health"])
def healthcheck():
    """
    Endpoint de verificación de salud del sistema.

    Trazabilidad: REQ-NF01
    """
    return {"status": "ok", "app": "AutoBhan Autopartes API", "version": "1.0.0"}
