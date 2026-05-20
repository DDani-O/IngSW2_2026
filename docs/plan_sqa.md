# Plan SQA — AutoBhan Autopartes
**Grupo 6 · Ingeniería de Software II · IUA 2026 · v1.0 · 20/05/2026**

## 1. Datos del proyecto

| Campo | Valor |
|-------|-------|
| Nombre | Gestión de AutoBhan Autopartes |
| Grupo | 6 |
| Integrantes | Bubica Hundt, Mirko · Nuñez, Celeste Aylen · Olguin, Daniel David |
| Repositorio | https://github.com/DDani-O/IngSW2_2026 |
| Versión | 1.0 — 20/05/2026 |

## 2. Propósito

Asegurar que el sistema AutoBhan cumpla los requerimientos definidos (REQ-F01 a REQ-F05, REQ-NF01 y REQ-NF02), manteniendo el código limpio, trazable y con pruebas suficientes durante las semanas 8 a 14 del cuatrimestre.

## 3. Roles

| Rol | Persona |
|-----|---------|
| QA — revisiones y estándares + Referente | Bubica Hundt, Mirko |
| QC — testing y defectos | Nuñez, Celeste Aylen |
| Documentador | Olguin, Daniel David |

## 4. Estándares y convenciones

| Aspecto | Convención |
|---------|-----------|
| Estilo backend | PEP 8 (Python) |
| Estilo frontend | Airbnb JavaScript Style Guide |
| Naming backend | snake_case (variables/funciones) · PascalCase (clases) |
| Naming frontend | camelCase (variables) · PascalCase (componentes) |
| Mensajes de commit | `[REQ-FXX] Descripción en infinitivo` |
| Indentación | 4 espacios (Python) · 2 espacios (JS/JSX) |
| Trazabilidad | Cada función lleva `Trazabilidad: REQ-FXX` en su docstring |

## 5. Revisiones

- Code review obligatorio antes de todo merge a `main`
- Al menos 1 aprobación de otro integrante
- `main` bloqueada para push directo

**Checklist de PR:**
- [ ] El código corre sin errores
- [ ] El linter no reporta errores críticos
- [ ] Los tests pasan
- [ ] Hay tests para el código nuevo
- [ ] No hay secrets hardcodeados
- [ ] El docstring tiene `Trazabilidad: REQ-FXX`

## 6. Métricas y umbrales

| Métrica | Umbral | Herramienta |
|---------|--------|-------------|
| CC máx por función | ≤ 10 | `radon cc . -a -s` |
| MI mínimo por módulo | ≥ 40 | `radon mi . -s` |
| Cobertura de tests | ≥ 60% | `pytest --cov` |
| Errores críticos linter | 0 | `flake8 --max-complexity=10` |

## 7. Herramientas

| Función | Herramienta |
|---------|-------------|
| Linter backend | flake8 |
| Linter frontend | ESLint (Airbnb) |
| Tests + cobertura | pytest + pytest-cov |
| Métricas CC/MI | radon |
| Versiones | Git + GitHub |

## 8. Frecuencia de medición

| Cuándo | Qué se verifica |
|--------|----------------|
| Cada commit | Linter local |
| Cada PR | Tests + cobertura + linter + checklist |
| Semanal | Métricas radon (CC, MI, LOC) |
| Antes de cada hito | Reporte completo + actualización del plan |

## 9. Gestión de defectos

- Todo defecto se carga como Issue en GitHub con severidad (Crítico/Mayor/Menor/Cosmético)
- Antes de cerrar un issue se escribe el test que verifica el fix
- No se mergea si hay issues críticos abiertos
- Cerrar con `Closes #N` en el commit

## 10. Criterios de aceptación — Hito 5

| Criterio | Umbral | OK |
|----------|--------|----|
| Tests pasan al 100% | 0 fallando | [ ] |
| Cobertura | ≥ 60% | [ ] |
| Issues críticos | 0 abiertos | [ ] |
| RTM completa | REQ-F01..F05 + NF01/NF02 | [ ] |
| README ejecutable | El docente puede correrlo | [ ] |
| Plan SQA actualizado | Versión final | [ ] |
| Plan de pruebas | ≥ 15 casos | [ ] |
| Wireframes | ≥ 3 baja + 2 alta fidelidad | [ ] |

## 11. Riesgos

| Riesgo | Prob. | Mitigación |
|--------|-------|-----------|
| Código sin trazabilidad | Alta | Docstring REQ-FXX obligatorio en todo PR |
| Cobertura < 60% al Hito 4 | Media | Tests junto al código en cada PR |
| CORS mal configurado | Alta | CORSMiddleware desde el primer commit |
| Conflictos de .env | Media | .env.example + README con setup paso a paso |

## 12. Cronograma

| Fecha | Tarea |
|-------|-------|
| 29/04 – 11/05 | Repo configurado, linter activo, primeros 5 tests |
| 12/05 – 19/05 | RTM v1 · métricas · code review activo |
| **20/05** | **★ HITO 3 — Plan SQA + métricas + linter** |
| 21/05 – 02/06 | Plan de pruebas · casos · reporte defectos |
| **03/06** | **★ HITO 4 — Pruebas + defectos + cobertura** |
| 04/06 – 15/06 | Wireframes · RTM completa · reflexión · SQA v3.0 |
| **16/06** | **★ HITO 5 — Entrega final + Defensa oral** |
