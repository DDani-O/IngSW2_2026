# Reporte de Defectos — Hito 4
**AutoBhan Autopartes — Grupo 6 — v1.0 — 03/06/2026**

> Los defectos fueron detectados durante el desarrollo y las sesiones de prueba.
> Cada uno fue cargado como Issue en GitHub y resuelto antes de mergearse a main.

---

## Tabla de defectos

| ID | Severidad | Título | Módulo | Estado |
|----|-----------|--------|--------|--------|
| DEF-001 | Mayor | Pre-commit hook no ejecuta en Windows (shebang Unix) | .githooks/pre-commit | Resuelto |
| DEF-002 | Mayor | Tests de historial fallan por ilike intermitente en Supabase | tests/test_historial.py | Resuelto |
| DEF-003 | Mayor | Duplicate key en test_crear_repuesto_exitoso al reusar numero_serie | tests/test_repuestos.py | Resuelto |
| DEF-004 | Mayor | CC de listar_historial = 11 supera umbral del Plan SQA (≤10) | routers/historial.py | Resuelto |
| DEF-006 | Menor | supabase_client.py falla al importar si no existe .env (conexión eager) | db/supabase_client.py | Resuelto |
| DEF-007 | Cosmético | Errores E302 y F401 en test_alertas.py detectados por flake8 | tests/test_alertas.py | Resuelto |

---

## Detalle por defecto

### DEF-001 — Pre-commit hook no ejecuta en Windows
**Severidad:** Mayor
**Descripción:** El pre-commit hook estaba escrito con shebang `#!/usr/bin/env python3` que Git en Windows no puede resolver. El commit se realizaba sin correr linter ni tests.
**Pasos para reproducir:**
1. Configurar `git config core.hooksPath .githooks`
2. Hacer un `git commit` en Windows
3. El hook se saltea sin error visible
**Fix aplicado:** Reescribir el hook como script `.bat` nativo para Windows más un wrapper `.py` multiplataforma.
**Commit:** `[QA] Agrega pre-commit.bat y pre-commit.py para compatibilidad Windows/Unix`

---

### DEF-002 — Tests de historial fallan por ilike intermitente
**Severidad:** Mayor
**Descripción:** `test_historial_filtro_empleado` usaba `.ilike()` de Supabase sobre el campo `empleado`. En ciertos momentos el worker de Cloudflare devuelve un error 1101 en vez de JSON, rompiendo el parseado de la respuesta.
**Pasos para reproducir:**
1. Correr `pytest tests/test_historial.py -v` repetidamente
2. En alguna ejecución `test_historial_filtro_empleado` falla con `JSONDecodeError`
**Fix aplicado:** El test ahora filtra por `repuesto_id` y verifica el empleado localmente, sin depender del `ilike` de la BD.
**Commit:** `[TESTS][FIX] Corrige test_historial_filtro_empleado`

---

### DEF-003 — Duplicate key en tests de repuestos
**Severidad:** Mayor
**Descripción:** El fixture de `test_crear_repuesto_exitoso` usaba un número de serie fijo `TEST-REP-9991`. Si el test fallaba antes del teardown, el registro quedaba en la BD y el siguiente intento lanzaba `23505 duplicate key`.
**Pasos para reproducir:**
1. Interrumpir los tests a mitad de ejecución (`Ctrl+C`)
2. Volver a correr `pytest` — `test_crear_repuesto_exitoso` falla con error de BD
**Fix aplicado:** El número de serie se genera con `f"TEST-{int(time.time())}"` — único por timestamp en cada ejecución.
**Commit:** `[TESTS][FIX] Usa timestamp en numero de serie de tests`

---

### DEF-004 — CC de listar_historial supera umbral del Plan SQA
**Severidad:** Mayor
**Descripción:** La función `listar_historial` tenía Complejidad Ciclomática = 11, un punto por encima del umbral de 10 definido en el Plan SQA. Detectado con `radon cc . -a -s`.
**Pasos para reproducir:**
```bash
radon cc routers/historial.py -s
# listar_historial - C (11)
```
**Fix aplicado:** Extracción de tres funciones auxiliares: `_aplicar_filtros()`, `_construir_detalle()` y `_obtener_repuestos_map()`. CC bajó a 6.
**Commit:** `[QA][REFACTOR] Baja CC de listar_historial de 11 a 6`

---

### DEF-006 — supabase_client.py falla al importar sin .env
**Severidad:** Menor
**Descripción:** La línea `supabase: Client = get_client()` al final del módulo ejecutaba la conexión en el momento de importar. Si no existía `.env`, cualquier import del módulo fallaba con `ValueError` antes de llegar al test.
**Pasos para reproducir:**
1. Borrar el `.env` del backend
2. Correr `pytest` — falla en el import con `ValueError: SUPABASE_URL debe estar definida`
**Fix aplicado:** Conexión lazy — el cliente se crea solo cuando se llama a `get_client()` por primera vez.
**Commit:** `[QA][FIX] Corrige tests de auth, hace conexion Supabase lazy`

---

### DEF-007 — Errores de linter en test_alertas.py
**Severidad:** Cosmético
**Descripción:** El pre-commit hook detectó dos errores en `tests/test_alertas.py`:
- `E302`: faltaba una línea en blanco antes de la función `test_stock_critico_retorna_solo_criticos`
- `F401`: import de `supabase` declarado pero no utilizado
**Pasos para reproducir:**
```bash
flake8 tests/test_alertas.py --max-complexity=10
# E302 expected 2 blank lines, found 1
# F401 'db.supabase_client.supabase' imported but unused
```
**Fix aplicado:** Se agregó la línea en blanco faltante y se eliminó el import sin usar.
**Commit:** `[QA][FIX] Corrige errores de linter en test_alertas.py`

---

## Métricas de defectos

| Severidad | Cantidad | Resueltos | Abiertos |
|-----------|----------|-----------|---------|
| Crítico | 0 | — | 0 |
| Mayor | 4 | 4 | 0 |
| Menor | 1 | 1 | 0 |
| Cosmético | 1 | 1 | 0 |
| **Total** | **6** | **6** | **0** |

**Densidad de defectos:** 6 defectos / 1.7 KLOC ≈ 3.5 defectos/KLOC
(meta industria: < 5 defectos/KLOC en módulos críticos ✅)
