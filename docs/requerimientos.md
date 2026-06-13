# Catálogo de Requerimientos — AutoBhan Autopartes
**Grupo 6 · Ingeniería de Software II · IUA 2026 · Basado en IEEE 830**

---

## Requerimientos Funcionales

| ID | Descripción | Prioridad | Fuente |
|----|-------------|-----------|--------|
| REQ-F01 | El sistema debe permitir registrar un repuesto con nombre, categoría (auto/moto/camioneta), marca, número de serie, precio y stock inicial. | Alta | Cliente |
| REQ-F02 | El sistema debe permitir registrar una entrada de stock (reposición) indicando el repuesto, la cantidad, proveedor, quién hizo la carga (empleado) y fecha. | Alta | Cliente |
| REQ-F03 | El sistema debe permitir registrar una salida de stock (venta o uso) indicando el repuesto, la cantidad, quién hizo el retiro (empleado) y finalidad, e impedir la operación si el stock resultante sería negativo. | Alta | Cliente |
| REQ-F04 | El sistema debe permitir consultar el stock actual de todos los repuestos, con filtros por categoría y nombre. | Alta | Cliente |
| REQ-F05 | El sistema debe listar todos los repuestos cuyo stock actual sea menor o igual al stock mínimo configurado ("stock crítico"). | Alta | Cliente |

---

## Requerimientos No Funcionales

| ID | Descripción | Umbral medible | Fuente |
|----|-------------|----------------|--------|
| REQ-NF01 | La consulta de stock no debe superar 2 segundos con hasta 500 repuestos registrados. | Tiempo de respuesta ≤ 2 seg | Consigna |
| REQ-NF02 | Los datos deben persistir en una base de datos relacional. Las credenciales nunca se exponen al cliente — toda comunicación con Supabase pasa por el backend. | BD PostgreSQL + auth vía backend | Consigna |

---

## Requerimientos de Restricción

| ID | Descripción |
|----|-------------|
| REQ-R01 | LOC objetivo: entre 800 y 3000 líneas de código (sin contar dependencias). |
| REQ-R02 | El docente debe poder ejecutar el proyecto siguiendo el README sin consultas adicionales. |
| REQ-R03 | El repositorio debe ser público en GitHub con al menos 10 commits descriptivos con formato `[REQ-FXX] Descripción`. |
