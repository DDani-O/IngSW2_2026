"""
Módulo: db/supabase_client.py
Responsabilidad: inicializar y exponer el cliente de Supabase.
Trazabilidad: REQ-NF02
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None


def get_client() -> Client:
    """
    Retorna el cliente de Supabase (singleton lazy).
    Se inicializa solo cuando se llama por primera vez.

    Trazabilidad: REQ-NF02
    """
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL y SUPABASE_KEY deben estar definidas en el .env"
            )
        _client = create_client(url, key)
    return _client


# Alias para compatibilidad — los routers llaman a _get_db() que usa este módulo
supabase = get_client  # se llama lazy en cada router via _get_db()
