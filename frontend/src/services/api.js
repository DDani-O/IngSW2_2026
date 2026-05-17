// services/api.js
// Responsabilidad: comunicación con el backend FastAPI.
// El frontend NUNCA habla directo con Supabase.
// Todas las credenciales viven en el backend.
// Trazabilidad: REQ-F01, REQ-F02, REQ-F03, REQ-F04, REQ-F05, REQ-NF02

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Token JWT guardado en memoria (no en localStorage por seguridad)
let _token = null;

export const setToken = (token) => { _token = token; };
export const clearToken = () => { _token = null; };
export const getToken = () => _token;

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (_token) headers['Authorization'] = `Bearer ${_token}`;

  const response = await fetch(`${BASE_URL}${path}`, { headers, ...options });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) return null;
  return response.json();
}

// Auth — login y logout pasan por el backend (REQ-NF02)
export const authService = {
  login: (email, password) => request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }),
  logout: () => request('/auth/logout', { method: 'POST' }),
};

// REQ-F01 y REQ-F04: gestión de repuestos
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
