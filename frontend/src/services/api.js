// services/api.js
// Responsabilidad: comunicación con el backend FastAPI.
// Trazabilidad: REQ-F01, REQ-F02, REQ-F03, REQ-F04, REQ-F05

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

// REQ-F01: gestión de repuestos
export const repuestosService = {
  listar: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/repuestos/${query ? `?${query}` : ''}`);
  },
  crear: (data) => request('/repuestos/', { method: 'POST', body: JSON.stringify(data) }),
  obtener: (id) => request(`/repuestos/${id}`),
  actualizar: (id, data) => request(`/repuestos/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
};

// REQ-F02: entrada de stock
export const entradaStockService = {
  registrar: (data) => request('/stock/entrada', { method: 'POST', body: JSON.stringify(data) }),
};

// REQ-F03: salida de stock
export const salidaStockService = {
  registrar: (data) => request('/stock/salida', { method: 'POST', body: JSON.stringify(data) }),
};

// REQ-F05: stock crítico
export const alertasService = {
  stockCritico: () => request('/alertas/stock-critico'),
};
