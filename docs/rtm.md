# Matriz de Trazabilidad de Requerimientos (RTM)
**AutoBhan Autopartes — Grupo 6 — v1.0 — 20/05/2026**

| REQ | Descripción | Módulo / Archivo | Función / Línea | Test(s) | Estado |
|-----|-------------|-----------------|-----------------|---------|--------|
| REQ-F01 | Registrar repuesto con nombre, categoría, marca, N° serie, precio y stock inicial | `routers/repuestos.py` | `crear_repuesto()` | TC-001, TC-002, TC-003 | Verificado |
| REQ-F01 | Obtener repuesto por ID | `routers/repuestos.py` | `obtener_repuesto()` | TC-004 | Verificado |
| REQ-F01 | Actualizar campos de repuesto | `routers/repuestos.py` | `actualizar_repuesto()` | — | Implementado |
| REQ-F02 | Registrar entrada de stock (reposición) | `routers/stock.py` | `registrar_entrada()` | TC-008, TC-009, TC-010 | Verificado |
| REQ-F03 | Registrar salida de stock e impedir stock negativo | `routers/stock.py` | `registrar_salida()` | TC-011, TC-012, TC-013 | Verificado |
| REQ-F04 | Consultar stock con filtros por categoría y nombre | `routers/repuestos.py` | `listar_repuestos()` | TC-005, TC-006, TC-007 | Verificado |
| REQ-F05 | Listar repuestos en stock crítico (stock ≤ mínimo) | `routers/alertas.py` | `listar_stock_critico()` | TC-014, TC-015, TC-016 | Verificado |
| REQ-NF01 | Consulta de stock < 2 seg con 500 repuestos | `main.py` | `healthcheck()` | TC-017 | Implementado |
| REQ-NF02 | Persistencia en base de datos relacional | `db/supabase_client.py` | `get_client()` | — | Implementado |

## Schemas (validación Pydantic)

| REQ | Archivo | Clase |
|-----|---------|-------|
| REQ-F01 | `schemas/repuesto.py` | `RepuestoCreate`, `RepuestoResponse`, `RepuestoUpdate` |
| REQ-F02 | `schemas/movimiento.py` | `EntradaStockCreate` |
| REQ-F03 | `schemas/movimiento.py` | `SalidaStockCreate` |
| REQ-F04 | `schemas/repuesto.py` | `RepuestoResponse` |
| REQ-F05 | `schemas/repuesto.py` | `RepuestoResponse` |

## Frontend

| REQ | Componente | Página |
|-----|-----------|--------|
| REQ-F01, REQ-F04 | `Repuestos.jsx` | `/repuestos` |
| REQ-F02, REQ-F03 | `Movimientos.jsx` | `/movimientos` |
| REQ-F04, REQ-F05 | `Dashboard.jsx` | `/dashboard` |
| REQ-NF02 | `Login.jsx` | `/` |

## Casos de prueba

| ID | REQ | Descripción | Tipo |
|----|-----|-------------|------|
| TC-001 | REQ-F01 | Crear repuesto con datos válidos → 201 | Caja negra |
| TC-002 | REQ-F01 | Crear repuesto con precio negativo → 422 | Valor límite |
| TC-003 | REQ-F01 | Crear repuesto con categoría inválida → 422 | Caja negra |
| TC-004 | REQ-F01 | Obtener repuesto con ID inexistente → 404 | Caja negra |
| TC-005 | REQ-F04 | Listar repuestos sin filtro → lista completa | Caja negra |
| TC-006 | REQ-F04 | Listar con filtro categoría=auto | Caja negra |
| TC-007 | REQ-F04 | Filtro con categoría inválida → 422 | Valor límite |
| TC-008 | REQ-F02 | Entrada de stock con datos válidos → 201 | Caja negra |
| TC-009 | REQ-F02 | Entrada con cantidad=0 → 422 | Valor límite |
| TC-010 | REQ-F02 | Entrada con repuesto inexistente → 404 | Caja negra |
| TC-011 | REQ-F03 | Salida con stock suficiente → 201 | Caja negra |
| TC-012 | REQ-F03 | Salida con cantidad > stock → 400 | Valor límite |
| TC-013 | REQ-F03 | Salida con cantidad == stock (exacto) → 201 | Valor límite |
| TC-014 | REQ-F05 | Stock crítico retorna solo repuestos críticos | Caja negra |
| TC-015 | REQ-F05 | Stock crítico incluye stock == mínimo | Valor límite |
| TC-016 | REQ-F05 | Stock crítico vacío si todos tienen stock OK | Caja negra |
| TC-017 | REQ-NF01 | Health check responde 200 con status ok | Caja blanca |

## Estado de gaps

| Situación | REQ afectado |
|-----------|-------------|
| `actualizar_repuesto` sin test | REQ-F01 — pendiente Hito 4 |
| REQ-NF01 rendimiento real (500 repuestos) | Pendiente test de performance Hito 4 |
| REQ-NF02 sin test de integración real | Pendiente Hito 4 con Supabase real |
