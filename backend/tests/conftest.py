"""
Módulo: tests/conftest.py
Responsabilidad: fixtures compartidos para la suite de tests.
Usa mocks del cliente Supabase para no depender de conexión real.
Trazabilidad: REQ-F01, REQ-F02, REQ-F03, REQ-F04, REQ-F05
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def make_supabase_mock(return_data=None):
    """Construye un mock del cliente Supabase que devuelve return_data."""
    mock_result = MagicMock()
    mock_result.data = return_data if return_data is not None else []

    mock_query = MagicMock()
    mock_query.execute.return_value = mock_result
    mock_query.eq.return_value = mock_query
    mock_query.ilike.return_value = mock_query
    mock_query.select.return_value = mock_query
    mock_query.insert.return_value = mock_query
    mock_query.update.return_value = mock_query

    mock_client = MagicMock()
    mock_client.table.return_value = mock_query
    return mock_client, mock_query, mock_result


@pytest.fixture
def cliente_api():
    """TestClient de FastAPI con Supabase mockeado."""
    mock_client, _, _ = make_supabase_mock()
    with patch("db.supabase_client.supabase", mock_client):
        from main import app
        with TestClient(app) as c:
            yield c, mock_client
