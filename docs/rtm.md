# Matriz de Trazabilidad de Requerimientos (RTM)
**AutoBhan Autopartes — Grupo 6 — v2.1 — 13/06/2026**

La RTM vincula cada requerimiento con su módulo de código, sus tests y su estado.
Una fila sin código = no implementado. Una fila sin tests = no verificado.

---

## 1. Trazabilidad principal

| REQ | Descripción | Módulo / Archivo | Función | Tests | Estado |
|-----|-------------|-----------------|---------|-------|--------|
| REQ-F01 | Registrar y gestionar repuestos | `routers/repuestos.py` | `crear_repuesto()` `obtener_repuesto()` `actualizar_repuesto()` | TC-CN-001…008, TC-CB-005 | Verificado |
| REQ-F02 | Registrar entrada de stock | `routers/stock.py` | `registrar_entrada()` | TC-CN-009…012, TC-CB-006 | Verificado |
| REQ-F03 | Registrar salida e impedir stock negativo | `routers/stock.py` | `registrar_salida()` | TC-CN-013…016, TC-CB-001, TC-CB-002 | Verificado |
| REQ-F04 | Consultar stock con filtros por categoría y nombre | `routers/repuestos.py` | `listar_repuestos()` | TC-CN-017…020 | Verificado |
| REQ-F05 | Listar repuestos en stock crítico (stock ≤ mínimo) | `routers/alertas.py` | `listar_stock_critico()` | TC-CN-021…023, TC-CB-003, TC-CB-004 | Verificado |
| REQ-NF01 | Consulta < 2 seg con 500 repuestos | `main.py`, `routers/repuestos.py` | `healthcheck()`, `listar_repuestos()` | TC-CN-024, TC-NF01-001 | Verificado |
| REQ-NF02 | Persistencia BD + login admin vía backend | `routers/auth.py` `db/supabase_client.py` | `login()` `logout()` `get_client()` | TC-CN-025…028, TC-CB-007 | Verificado |

---

## 2. Trazabilidad en schemas (Pydantic)

| REQ | Archivo | Clases |
|-----|---------|--------|
| REQ-F01 | `schemas/repuesto.py` | `RepuestoCreate`, `RepuestoResponse`, `RepuestoUpdate` |
| REQ-F02 | `schemas/movimiento.py` | `EntradaStockCreate`, `MovimientoResponse` |
| REQ-F03 | `schemas/movimiento.py` | `SalidaStockCreate`, `MovimientoResponse` |
| REQ-F04 | `schemas/repuesto.py` | `RepuestoResponse` |
| REQ-F05 | `schemas/repuesto.py` | `RepuestoResponse` |

---

## 3. Trazabilidad en frontend (React)

| REQ | Componente | Página / Ruta |
|-----|-----------|---------------|
| REQ-F01, REQ-F04 | `Repuestos.jsx` | `/repuestos` — listado, filtros y registro |
| REQ-F02, REQ-F03 | `Movimientos.jsx` | `/movimientos` — entradas y salidas |
| REQ-F02, REQ-F03 | `Historial.jsx` | `/historial` — historial con filtros |
| REQ-F04, REQ-F05 | `Dashboard.jsx` | `/dashboard` — resumen y stock crítico |
| REQ-NF02 | `Login.jsx` | `/` — autenticación vía backend |

---

## 4. Casos de prueba

### Caja negra (TC-CN)

| ID | REQ | Técnica | Entrada / Condición | Resultado esperado | Estado |
|----|-----|---------|--------------------|--------------------|--------|
| TC-CN-001 | REQ-F01 | Partición válida | nombre, cat=auto, precio=1500, stock=10 | HTTP 201, repuesto creado | Pasa |
| TC-CN-002 | REQ-F01 | Valor límite | precio = -1 | HTTP 422 | Pasa |
| TC-CN-003 | REQ-F01 | Valor límite | precio = 0 | HTTP 422 | Pasa |
| TC-CN-004 | REQ-F01 | Partición inválida | categoria = barco | HTTP 422 | Pasa |
| TC-CN-005 | REQ-F01 | Partición inválida | GET /repuestos/999999 | HTTP 404 | Pasa |
| TC-CN-006 | REQ-F01 | Partición válida | PATCH precio=2500, stock_minimo=4 | HTTP 200, actualizado | Pasa |
| TC-CN-007 | REQ-F01 | Partición inválida | PATCH sin campos | HTTP 400 | Pasa |
| TC-CN-008 | REQ-F01 | Valor límite | PATCH precio=-50 | HTTP 422 | Pasa |
| TC-CN-009 | REQ-F02 | Partición válida | cantidad=5, stock pasa a 15 | HTTP 201 | Pasa |
| TC-CN-010 | REQ-F02 | Valor límite | cantidad = 0 | HTTP 422 | Pasa |
| TC-CN-011 | REQ-F02 | Valor límite | cantidad = 1 (mínimo válido) | HTTP 201 | Pasa |
| TC-CN-012 | REQ-F02 | Partición inválida | repuesto_id=999999 | HTTP 404 | Pasa |
| TC-CN-013 | REQ-F03 | Partición válida | cantidad=3, stock pasa de 10 a 7 | HTTP 201 | Pasa |
| TC-CN-014 | REQ-F03 | Valor límite | cantidad=10 (stock exacto) | HTTP 201, stock=0 | Pasa |
| TC-CN-015 | REQ-F03 | Valor límite | cantidad=11 (uno más que el stock) | HTTP 400 | Pasa |
| TC-CN-016 | REQ-F03 | Partición inválida | cantidad=100, stock=2 | HTTP 400 | Pasa |
| TC-CN-017 | REQ-F04 | Tabla de decisión | Sin filtros | Lista completa ≥ 12 items | Pasa |
| TC-CN-018 | REQ-F04 | Tabla de decisión | categoria=auto | Solo repuestos de auto | Pasa |
| TC-CN-019 | REQ-F04 | Tabla de decisión | categoria=moto | Solo repuestos de moto | Pasa |
| TC-CN-020 | REQ-F04 | Partición inválida | categoria=barco | HTTP 422 | Pasa |
| TC-CN-021 | REQ-F05 | Valor límite | stock=2, min=5 (stock < min) | Aparece en /alertas/stock-critico | Pasa |
| TC-CN-022 | REQ-F05 | Valor límite | stock=5, min=5 (exacto) | Aparece en /alertas/stock-critico | Pasa |
| TC-CN-023 | REQ-F05 | Valor límite | stock=12, min=5 (stock > min) | NO aparece en /alertas/stock-critico | Pasa |
| TC-CN-024 | REQ-NF01 | Caja negra | GET /health | HTTP 200, status=ok | Pasa |
| TC-CN-025 | REQ-NF02 | Tabla de decisión | POST /auth/login creds válidas | HTTP 200 + JWT | Pasa |
| TC-CN-026 | REQ-NF02 | Tabla de decisión | POST /auth/login creds inválidas | HTTP 401 | Pasa |
| TC-CN-027 | REQ-NF02 | Partición inválida | POST /auth/login email malformado | HTTP 422 | Pasa |
| TC-CN-028 | REQ-NF02 | Caja negra | POST /auth/logout | HTTP 204 | Pasa |

### Caja blanca (TC-CB)

| ID | REQ | Rama analizada | Archivo | Resultado esperado | Estado |
|----|-----|---------------|---------|-------------------|--------|
| TC-CB-001 | REQ-F03 | `if stock_resultante < 0 → True` | `routers/stock.py` L76 | HTTP 400 | Pasa |
| TC-CB-002 | REQ-F03 | `if stock_resultante < 0 → False` | `routers/stock.py` L76 | HTTP 201 | Pasa |
| TC-CB-003 | REQ-F05 | `if stock_actual <= stock_minimo → True` | `routers/alertas.py` L28 | Repuesto incluido | Pasa |
| TC-CB-004 | REQ-F05 | `if stock_actual <= stock_minimo → False` | `routers/alertas.py` L28 | Repuesto excluido | Pasa |
| TC-CB-005 | REQ-F01 | `if not payload → True` | `routers/repuestos.py` L77 | HTTP 400 | Pasa |
| TC-CB-006 | REQ-F02 | `if not result.data` (rep. no existe) | `routers/stock.py` L32 | HTTP 404 | Pasa |
| TC-CB-007 | REQ-NF02 | `if not result.session → True` | `routers/auth.py` L48 | HTTP 401 | Pasa |

---

## 5. Gaps identificados

No hay gaps abiertos. El último gap (REQ-NF01 — test de rendimiento real con 500 repuestos) fue resuelto el 13/06/2026: se generaron 279 repuestos adicionales (series `SEED-AU/MO/CA-XXXX`) y 150 movimientos asociados, alcanzando 562 repuestos y 612 movimientos en la base de datos real de Supabase. El test `TC-NF01-001` verifica que `GET /repuestos/` con 562 repuestos responde en ~0.19s promedio (máx. 0.21s), muy por debajo del umbral de 2 segundos.
