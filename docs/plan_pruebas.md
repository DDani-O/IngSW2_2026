# Plan de Pruebas — Hito 4
**AutoBhan Autopartes — Grupo 6 — v1.0 — 03/06/2026**

---

## 1. Alcance

### Qué se testea
- REQ-F01: registro, consulta y actualización de repuestos
- REQ-F02: registro de entradas de stock
- REQ-F03: registro de salidas de stock con validación de negativos
- REQ-F04: consulta de stock con filtros por categoría y nombre
- REQ-F05: listado de repuestos en stock crítico
- REQ-NF01: respuesta del sistema (healthcheck)
- REQ-NF02: autenticación de administrador vía backend

### Qué NO se testea
- Interfaz de usuario (frontend React) — se valida manualmente
- Rendimiento bajo carga (500 repuestos simultáneos) — fuera del alcance del Hito 4
- Seguridad avanzada (penetration testing, inyección SQL) — fuera del alcance

---

## 2. Estrategia

### Tipos de prueba aplicados

| Tipo | Técnica | Herramienta | Módulos |
|------|---------|-------------|---------|
| Caja negra — Partición de equivalencia | Clases válidas e inválidas por campo | pytest | Todos los routers |
| Caja negra — Valores límite | Bordes de cantidad, precio, stock | pytest | stock.py, repuestos.py |
| Caja negra — Tabla de decisión | Combinaciones de filtros | pytest | repuestos.py, historial.py |
| Caja blanca — Cobertura de ramas | Ramas if/else en cada función | pytest-cov | stock.py, alertas.py |
| Integración real | Tests contra Supabase PostgreSQL real | pytest + Supabase | Todos |

### Niveles de prueba

- **Unitaria:** cada endpoint de forma aislada con datos controlados
- **Integración:** todos los tests corren contra la BD real de Supabase
- **Sistema:** validación manual del flujo completo en el frontend

---

## 3. Criterios de aceptación

| Criterio | Umbral | Estado |
|----------|--------|--------|
| Tests pasando | 100% | ✅ 34/34 |
| Cobertura módulos principales | ≥ 60% | ✅ 95% |
| Errores de linter | 0 | ✅ 0 |
| CC máximo por función | ≤ 10 | ✅ máx 6 |
| Issues críticos abiertos | 0 | ✅ 0 |

### Criterio de entrada (para ejecutar las pruebas)
- El backend levanta sin errores con `uvicorn main:app --reload`
- El `.env` tiene las credenciales de Supabase configuradas
- La base de datos tiene al menos los 13 repuestos del seed

### Criterio de salida (para considerar el ciclo de pruebas completo)
- Todos los casos de prueba ejecutados
- 0 tests fallando
- Defectos detectados cargados como Issues en GitHub con severidad asignada

---

## 4. Casos de prueba

### Convención de ID

| Prefijo | Tipo |
|---------|------|
| TC-CN-XXX | Caja negra |
| TC-CB-XXX | Caja blanca |

---

### REQ-F01 — Registro y gestión de repuestos

**Técnica: Partición de equivalencia + Valores límite**

Particiones identificadas para `precio`:
- Inválido: ≤ 0
- Válido: > 0

Particiones para `categoria`:
- Válida: `auto`, `moto`, `camioneta`
- Inválida: cualquier otro string

| ID | REQ | Técnica | Precondición | Entrada | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|---------|-------------------|----------------|--------|
| TC-CN-001 | REQ-F01 | Partición válida | BD disponible | nombre="Filtro", categoria="auto", marca="Bosch", precio=1500, stock=10 | HTTP 201, repuesto creado | HTTP 201 ✅ | Pasa |
| TC-CN-002 | REQ-F01 | Valor límite | BD disponible | precio=-1 (inválido) | HTTP 422 | HTTP 422 ✅ | Pasa |
| TC-CN-003 | REQ-F01 | Valor límite | BD disponible | precio=0 (inválido) | HTTP 422 | HTTP 422 ✅ | Pasa |
| TC-CN-004 | REQ-F01 | Partición inválida | BD disponible | categoria="barco" | HTTP 422 | HTTP 422 ✅ | Pasa |
| TC-CN-005 | REQ-F01 | Partición inválida | Repuesto inexistente | GET /repuestos/999999 | HTTP 404 | HTTP 404 ✅ | Pasa |
| TC-CN-006 | REQ-F01 | Partición válida | Repuesto existente | PATCH precio=2500, stock_minimo=4 | HTTP 200, campos actualizados | HTTP 200 ✅ | Pasa |
| TC-CN-007 | REQ-F01 | Partición inválida | Repuesto existente | PATCH sin campos | HTTP 400 | HTTP 400 ✅ | Pasa |
| TC-CN-008 | REQ-F01 | Valor límite | Repuesto existente | PATCH precio=-50 | HTTP 422 | HTTP 422 ✅ | Pasa |

---

### REQ-F02 — Entrada de stock

**Técnica: Partición de equivalencia + Valores límite**

Particiones para `cantidad`:
- Inválida: ≤ 0
- Válida: ≥ 1

| ID | REQ | Técnica | Precondición | Entrada | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|---------|-------------------|----------------|--------|
| TC-CN-009 | REQ-F02 | Partición válida | Repuesto existe, stock=10 | cantidad=5, proveedor="Sur", empleado="Mirko" | HTTP 201, stock=15 | HTTP 201 ✅ | Pasa |
| TC-CN-010 | REQ-F02 | Valor límite | Repuesto existe | cantidad=0 | HTTP 422 | HTTP 422 ✅ | Pasa |
| TC-CN-011 | REQ-F02 | Valor límite | Repuesto existe | cantidad=1 (mínimo válido) | HTTP 201 | HTTP 201 ✅ | Pasa |
| TC-CN-012 | REQ-F02 | Partición inválida | Repuesto inexistente | repuesto_id=999999, cantidad=5 | HTTP 404 | HTTP 404 ✅ | Pasa |

---

### REQ-F03 — Salida de stock

**Técnica: Partición de equivalencia + Valores límite**

Particiones para `cantidad` relativa al stock actual:
- Inválida: cantidad > stock_actual (genera negativo)
- Límite exacto: cantidad == stock_actual
- Válida: cantidad < stock_actual

| ID | REQ | Técnica | Precondición | Entrada | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|---------|-------------------|----------------|--------|
| TC-CN-013 | REQ-F03 | Partición válida | Repuesto existe, stock=10 | cantidad=3, empleado="Celeste", finalidad="venta" | HTTP 201, stock=7 | HTTP 201 ✅ | Pasa |
| TC-CN-014 | REQ-F03 | Valor límite | Repuesto existe, stock=10 | cantidad=10 (exacto) | HTTP 201, stock=0 | HTTP 201 ✅ | Pasa |
| TC-CN-015 | REQ-F03 | Valor límite | Repuesto existe, stock=10 | cantidad=11 (uno más) | HTTP 400 "Stock insuficiente" | HTTP 400 ✅ | Pasa |
| TC-CN-016 | REQ-F03 | Partición inválida | Repuesto existe, stock=2 | cantidad=100 | HTTP 400 "Stock insuficiente" | HTTP 400 ✅ | Pasa |

---

### REQ-F04 — Consulta de stock con filtros

**Técnica: Tabla de decisión (combinaciones de filtros)**

| ID | REQ | Técnica | Precondición | Filtros aplicados | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|-------------------|-------------------|----------------|--------|
| TC-CN-017 | REQ-F04 | Tabla de decisión | ≥12 repuestos en BD | Sin filtros | Lista completa ≥ 12 items | Lista ✅ | Pasa |
| TC-CN-018 | REQ-F04 | Tabla de decisión | Repuestos de "auto" en BD | categoria=auto | Solo repuestos de auto | Filtrado ✅ | Pasa |
| TC-CN-019 | REQ-F04 | Tabla de decisión | Repuestos de "moto" en BD | categoria=moto | Solo repuestos de moto | Filtrado ✅ | Pasa |
| TC-CN-020 | REQ-F04 | Partición inválida | BD disponible | categoria=barco | HTTP 422 | HTTP 422 ✅ | Pasa |

---

### REQ-F05 — Stock crítico

**Técnica: Valores límite (stock_actual vs stock_minimo)**

Casos de borde:
- stock_actual < stock_minimo → CRÍTICO
- stock_actual == stock_minimo → CRÍTICO (límite exacto)
- stock_actual > stock_minimo → NO crítico

| ID | REQ | Técnica | Precondición | Condición | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|-----------|-------------------|----------------|--------|
| TC-CN-021 | REQ-F05 | Valor límite | Repuesto con stock=2, min=5 | stock < min | Aparece en /alertas/stock-critico | Aparece ✅ | Pasa |
| TC-CN-022 | REQ-F05 | Valor límite | Repuesto con stock=5, min=5 | stock == min (exacto) | Aparece en /alertas/stock-critico | Aparece ✅ | Pasa |
| TC-CN-023 | REQ-F05 | Valor límite | Repuesto con stock=12, min=5 | stock > min | NO aparece en /alertas/stock-critico | No aparece ✅ | Pasa |

---

### REQ-NF01 y REQ-NF02 — No funcionales

| ID | REQ | Técnica | Precondición | Acción | Resultado esperado | Resultado real | Estado |
|----|-----|---------|-------------|--------|-------------------|----------------|--------|
| TC-CN-024 | REQ-NF01 | Caja negra | App levantada | GET /health | HTTP 200, status="ok" | HTTP 200 ✅ | Pasa |
| TC-CN-025 | REQ-NF02 | Tabla de decisión | Usuario admin en Supabase | POST /auth/login con creds válidas | HTTP 200 + JWT | HTTP 200 ✅ | Pasa |
| TC-CN-026 | REQ-NF02 | Tabla de decisión | — | POST /auth/login con creds inválidas | HTTP 401 | HTTP 401 ✅ | Pasa |
| TC-CN-027 | REQ-NF02 | Partición inválida | — | POST /auth/login email malformado | HTTP 422 | HTTP 422 ✅ | Pasa |
| TC-CN-028 | REQ-NF02 | Caja negra | Sesión activa | POST /auth/logout | HTTP 204 | HTTP 204 ✅ | Pasa |

---

### Casos de caja blanca — Cobertura de ramas

**Técnica: cobertura de sentencias y ramas clave**

| ID | REQ | Rama analizada | Archivo | Resultado esperado | Resultado real | Estado |
|----|-----|---------------|---------|-------------------|----------------|--------|
| TC-CB-001 | REQ-F03 | `if stock_resultante < 0` → True | routers/stock.py:L76 | HTTP 400 | HTTP 400 ✅ | Pasa |
| TC-CB-002 | REQ-F03 | `if stock_resultante < 0` → False | routers/stock.py:L76 | HTTP 201 | HTTP 201 ✅ | Pasa |
| TC-CB-003 | REQ-F05 | `if r["stock_actual"] <= r["stock_minimo"]` → True | routers/alertas.py:L28 | Repuesto incluido | Incluido ✅ | Pasa |
| TC-CB-004 | REQ-F05 | `if r["stock_actual"] <= r["stock_minimo"]` → False | routers/alertas.py:L28 | Repuesto excluido | Excluido ✅ | Pasa |
| TC-CB-005 | REQ-F01 | `if not payload` → True (sin campos) | routers/repuestos.py:L77 | HTTP 400 | HTTP 400 ✅ | Pasa |
| TC-CB-006 | REQ-F02 | `if not result.data` (repuesto no existe) | routers/stock.py:L32 | HTTP 404 | HTTP 404 ✅ | Pasa |
| TC-CB-007 | REQ-NF02 | `if not result.session` → True | routers/auth.py:L48 | HTTP 401 | HTTP 401 ✅ | Pasa |

---

## 5. Resumen de cobertura

| Módulo | Cobertura | Tests asociados |
|--------|-----------|----------------|
| routers/repuestos.py | 91% | TC-CN-001…008, TC-CB-005 |
| routers/stock.py | 94% | TC-CN-009…016, TC-CB-001…002, TC-CB-006 |
| routers/alertas.py | 100% | TC-CN-021…023, TC-CB-003…004 |
| routers/auth.py | 85% | TC-CN-025…028, TC-CB-007 |
| routers/historial.py | 93% | (tests de historial) |
| **TOTAL** | **95%** | **34 tests automatizados** |
