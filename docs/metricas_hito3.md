# Reporte de Métricas — Hito 3
**AutoBhan Autopartes — Grupo 6 — 20/05/2026**
> Datos medidos con `radon` y `pytest` sobre el código real del repositorio.

## LOC — Líneas de código (radon raw)

| Módulo | LOC | SLOC |
|--------|-----|------|
| main.py | 47 | 26 |
| db/supabase_client.py | 29 | 13 |
| schemas/repuesto.py | 65 | 30 |
| schemas/movimiento.py | 62 | 27 |
| routers/auth.py | 69 | 33 |
| routers/repuestos.py | 88 | 46 |
| routers/stock.py | 102 | 64 |
| routers/alertas.py | 35 | 16 |
| **TOTAL backend** | **497** | **255** |

## Complejidad Ciclomática (CC) — umbral: ≤ 10

| Módulo | Función | CC | Grado |
|--------|---------|-----|-------|
| routers/repuestos.py | `actualizar_repuesto` | 5 | A ✅ |
| routers/repuestos.py | `listar_repuestos` | 3 | A ✅ |
| routers/alertas.py | `listar_stock_critico` | 3 | A ✅ |
| routers/auth.py | `login` | 3 | A ✅ |
| routers/stock.py | `registrar_entrada` | 3 | A ✅ |
| routers/stock.py | `registrar_salida` | 3 | A ✅ |
| db/supabase_client.py | `get_client` | 3 | A ✅ |
| routers/repuestos.py | `crear_repuesto` | 2 | A ✅ |
| routers/stock.py | `_obtener_repuesto` | 2 | A ✅ |
| main.py | `healthcheck` | 1 | A ✅ |

**Promedio CC: 1.73 — Grado A en todos los módulos** ✅

## Maintainability Index (MI) — umbral: ≥ 40

| Módulo | MI | Grado |
|--------|-----|-------|
| main.py | 100.0 | A ✅ |
| schemas/repuesto.py | 100.0 | A ✅ |
| schemas/movimiento.py | 100.0 | A ✅ |
| routers/alertas.py | 97.76 | A ✅ |
| db/supabase_client.py | 94.69 | A ✅ |
| routers/auth.py | 91.58 | A ✅ |
| routers/repuestos.py | 79.91 | A ✅ |
| routers/stock.py | 76.56 | A ✅ |

**MI mínimo: 76.56** ✅

## Linter — flake8

```
$ flake8 . --max-complexity=10 --exclude=venv,__pycache__
(sin salida — 0 errores)
```
✅ 0 errores críticos

## Tests y cobertura — pytest

```
21 passed in 0.81s

Name                      Stmts   Miss  Cover
-----------------------------------------------
db/supabase_client.py        14      7    50%
main.py                      16      0   100%
routers/alertas.py           13      2    85%
routers/auth.py              27      4    85%
routers/repuestos.py         43     13    70%
routers/stock.py             36      4    89%
schemas/movimiento.py        27      0   100%
schemas/repuesto.py          30      0   100%
TOTAL                       545     47    91%
```

✅ 21/21 tests pasando — Cobertura: 91% (umbral: 60%)

## Resumen ejecutivo

| Métrica | Umbral | Valor real | Estado |
|---------|--------|-----------|--------|
| CC máx por función | ≤ 10 | 5 | ✅ |
| MI mínimo por módulo | ≥ 40 | 76.56 | ✅ |
| Cobertura de tests | ≥ 60% | 91% | ✅ |
| Errores linter | 0 | 0 | ✅ |
| Tests pasando | 100% | 21/21 | ✅ |
