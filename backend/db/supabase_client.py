"""
Módulo: db/supabase_client.py
Responsabilidad: inicializar y exponer el cliente de Supabase.
Trazabilidad: REQ-NF02
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_client() -> Client:
    """
    Retorna el cliente de Supabase inicializado con las variables de entorno.

    Trazabilidad: REQ-NF02
    """
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        raise ValueError(
            "SUPABASE_URL y SUPABASE_KEY deben estar definidas en el .env"
        )
    return create_client(url, key)


supabase: Client = get_client()
