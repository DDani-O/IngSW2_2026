# AutoBhan Autopartes — Sistema de Gestión de Inventario

Sistema web para gestión de stock de repuestos de automotores (autos, motos, camionetas).  
Proyecto integrador — Ingeniería de Software II — IUA 2026 — Grupo 6.

🚀 **Demo en producción:** [frontend-production-fd897.up.railway.app](https://frontend-production-fd897.up.railway.app)

---

## Integrantes

| Nombre | Rol |
|--------|-----|
| Bubica Hundt, Mirko | QA — revisiones y estándares |
| Nuñez, Celeste Aylen | QC — testing y defectos |
| Olguin, Daniel David | Documentador + Referente |

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python + FastAPI + Uvicorn | Python 3.12 |
| Frontend | React + Vite | React 18 |
| Base de datos | Supabase (PostgreSQL) | — |
| Cliente BD | supabase-py | 2.4.3 |
| Auth | Supabase Auth vía backend | — |
| Deploy | Railway (2 servicios) | — |

---

## Requisitos previos

- Python 3.12+
- Node.js 18+
- Cuenta en Supabase con proyecto creado

---

## Instalación — Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

> `requirements.txt` contiene solo las dependencias de producción (FastAPI, uvicorn, supabase, pydantic).  
> `requirements-dev.txt` agrega las de desarrollo: pytest, pytest-cov, httpx, flake8, radon.

Creá un archivo `.env` en `backend/` con las siguientes variables:

```dotenv
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
APP_ENV=development
CORS_ORIGINS=http://localhost:5173
```

```bash
uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`  
Documentación automática (Swagger): `http://localhost:8000/docs`

---

## Instalación — Frontend

```bash
cd frontend
npm install
```

Creá un archivo `.env` en `frontend/` con:

```dotenv
VITE_API_URL=http://localhost:8000
```

```bash
npm run dev
```

El frontend queda disponible en `http://localhost:5173`

> ⚠️ El frontend **nunca** debe tener credenciales de Supabase. Toda comunicación con
> Supabase pasa por el backend (REQ-NF02).

---

## Configurar pre-commit hook (obligatorio, una sola vez)

El repositorio incluye un hook que corre **flake8 y pytest automáticamente** antes de cada commit. Si alguno falla, el commit se cancela.

**Windows (PowerShell):**
```powershell
.\setup-hooks.ps1
```

> Si PowerShell bloquea el script con `running scripts is disabled on this system`
> (política de ejecución por defecto), corré directamente:
> ```powershell
> git config core.hooksPath .githooks
> ```

**Mac/Linux:**
```bash
sh setup-hooks.sh
```

---

## Ejecutar tests

```bash
cd backend
pytest --cov=. --cov-report=term-missing
```

Resultado esperado: **34/34 tests pasando — 95% cobertura**

## Ejecutar linter

```bash
cd backend
flake8 . --max-complexity=10
```

## Métricas de complejidad

```bash
cd backend
radon cc . -a -s    # Complejidad Ciclomática (umbral: ≤ 10)
radon mi . -s       # Maintainability Index (umbral: ≥ 40)
radon raw . -s      # Líneas de código (objetivo: 800–3000)
```

---

## Ejemplos de uso de la API

Con el backend corriendo en `http://localhost:8000` (también disponible en `/docs` con Swagger):

### Crear un repuesto — REQ-F01

```bash
curl -X POST http://localhost:8000/repuestos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Filtro de aceite",
    "categoria": "auto",
    "marca": "Bosch",
    "numero_serie": "BO-FA-001",
    "precio": 1500,
    "stock_inicial": 12,
    "stock_minimo": 5
  }'
```

Respuesta `201 Created`:
```json
{
  "id": 1,
  "nombre": "Filtro de aceite",
  "categoria": "auto",
  "marca": "Bosch",
  "numero_serie": "BO-FA-001",
  "precio": 1500.0,
  "stock_actual": 12,
  "stock_minimo": 5
}
```

### Actualizar un repuesto — REQ-F01

```bash
curl -X PATCH http://localhost:8000/repuestos/1 \
  -H "Content-Type: application/json" \
  -d '{"precio": 1800, "stock_minimo": 3}'
```

Acepta cualquier combinación de: `nombre`, `categoria`, `marca`, `numero_serie`, `precio`, `stock_minimo`.

### Eliminar un repuesto — REQ-F01

```bash
curl -X DELETE http://localhost:8000/repuestos/1
```

Respuesta `204 No Content`. Los movimientos asociados se eliminan automáticamente (CASCADE).

### Registrar entrada de stock — REQ-F02

```bash
curl -X POST http://localhost:8000/stock/entrada \
  -H "Content-Type: application/json" \
  -d '{
    "repuesto_id": 1,
    "cantidad": 10,
    "proveedor": "Distribuidora Sur SRL",
    "empleado": "Mirko Bubica",
    "fecha": "2026-06-14"
  }'
```

### Registrar salida de stock — REQ-F03

```bash
curl -X POST http://localhost:8000/stock/salida \
  -H "Content-Type: application/json" \
  -d '{
    "repuesto_id": 1,
    "cantidad": 3,
    "empleado": "Celeste Nuñez",
    "finalidad": "venta"
  }'
```

Si `cantidad` supera el `stock_actual`, responde `400 Bad Request` con detalle `"Stock insuficiente"`.

### Consultar stock con filtros — REQ-F04

```bash
curl "http://localhost:8000/repuestos/?categoria=auto"
curl "http://localhost:8000/repuestos/?nombre=filtro"
```

### Listar repuestos en stock crítico — REQ-F05

```bash
curl http://localhost:8000/alertas/stock-critico
```

Respuesta `200 OK`: lista de repuestos cuyo `stock_actual <= stock_minimo`.

### Login de administrador — REQ-NF02

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@autobhan.com", "password": "********"}'
```

Responde `200 OK` con JWT o `401 Unauthorized` si las credenciales son inválidas.

---


## Ejecutar casos de prueba manualmente (curl)

Comandos base para ejecutar los casos de prueba desde la terminal. Reemplazá los valores según cada caso. Funcionan tanto contra local (`http://localhost:8000`) como contra producción (`https://backend-production-052ad.up.railway.app`).

### GET — consultar recursos

```bash
curl -s -X GET "https://backend-production-052ad.up.railway.app/repuestos/" \
  -w "\nHTTP: %{http_code}\n"
```

### POST — crear / registrar

```bash
curl -s -X POST "https://backend-production-052ad.up.railway.app/repuestos/" \
  -H "Content-Type: application/json" \
  -d '{"campo": "valor"}' \
  -w "\nHTTP: %{http_code}\n"
```

### PATCH — actualizar parcialmente

```bash
curl -s -X PATCH "https://backend-production-052ad.up.railway.app/repuestos/{id}" \
  -H "Content-Type: application/json" \
  -d '{"campo": "valor"}' \
  -w "\nHTTP: %{http_code}\n"
```

### DELETE — eliminar

```bash
curl -s -X DELETE "https://backend-production-052ad.up.railway.app/repuestos/{id}" \
  -w "\nHTTP: %{http_code}\n"
```

### Endpoints disponibles

| Endpoint | Métodos |
|----------|---------|
| `/repuestos/` | GET, POST |
| `/repuestos/{id}` | GET, PATCH, DELETE |
| `/stock/entrada` | POST |
| `/stock/salida` | POST |
| `/alertas/stock-critico` | GET |
| `/historial/` | GET |
| `/auth/login` | POST |
| `/auth/logout` | POST |
| `/health` | GET |

> **Flags:** `-s` silencia el progreso · `-H` define el header · `-d` es el body JSON · `-w` imprime el código HTTP al final.

## Variables de entorno

### Backend (`backend/.env`)

| Variable | Descripción |
|----------|-------------|
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | Anon key de Supabase |
| `APP_ENV` | `development` o `production` |
| `CORS_ORIGINS` | Origen permitido para CORS (URL del frontend) |

### Frontend (`frontend/.env`)

| Variable | Descripción |
|----------|-------------|
| `VITE_API_URL` | URL base del backend (FastAPI) |

---

## Deploy en Railway

El proyecto corre como **dos servicios** dentro del mismo proyecto de Railway.

### Backend

1. **New Service → Deploy from GitHub repo** → seleccionar este repositorio
2. **Settings → Root Directory** → `backend`
3. Railway detecta Python 3.12 via `runtime.txt` e instala `requirements.txt` automáticamente
4. El `Procfile` define el comando de arranque:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Variables** → agregar:

| Variable | Valor |
|----------|-------|
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | Anon key de Supabase |
| `APP_ENV` | `production` |
| `CORS_ORIGINS` | URL del frontend en Railway (con `https://`) |

### Frontend

1. **New Service → Deploy from GitHub repo** → mismo repositorio
2. **Settings → Root Directory** → `frontend`
3. **Build Command** → `npm run build`
4. **Start Command** → `npm run preview`
5. **Variables** → agregar `VITE_API_URL` con la URL del backend (con `https://`)

### Orden recomendado

1. Deployar el **backend** primero
2. Copiar la URL pública del backend
3. Deployar el **frontend** con `VITE_API_URL` apuntando al backend
4. Copiar la URL pública del frontend
5. Actualizar `CORS_ORIGINS` en el backend con la URL del frontend

---

## Decisiones de diseño

### Auth vía backend (no directa a Supabase)
El frontend nunca habla directamente con Supabase. Todo pasa por el backend (FastAPI), que maneja las credenciales en el servidor. Esto evita exponer el `anon key` en el bundle de React (las variables `VITE_*` quedan visibles en el cliente).

### Tests con base de datos real
Elegimos testear contra Supabase real en vez de mocks. Es más lento pero detecta bugs que los mocks esconden (FK constraints, tipos de datos, RLS). Para evitar colisiones entre tests, cada test genera números de serie únicos por timestamp en milliseconds (`TEST-{int(time.time() * 1000)}`).

### Separación de requirements de producción y dev
`requirements.txt` solo tiene las dependencias necesarias para correr el servidor (FastAPI, uvicorn, supabase, pydantic). `requirements-dev.txt` agrega las de testing y métricas (pytest, flake8, radon). Esto reduce el tiempo de build en Railway y la superficie de ataque en producción.

### RLS en Supabase
La base de datos tiene Row Level Security activo en todas las tablas. Se definieron políticas explícitas para SELECT, INSERT, UPDATE y DELETE (tanto para el rol `anon` como para `authenticated`). Sin una política para un verbo, Supabase bloquea la operación silenciosamente.

### ON DELETE CASCADE en movimientos
La FK `movimientos.repuesto_id → repuestos.id` está configurada con `ON DELETE CASCADE`. Al eliminar un repuesto, sus movimientos asociados se eliminan automáticamente. Esto mantiene la integridad referencial sin necesidad de lógica adicional en el backend.

### Conexión lazy a Supabase
El cliente de Supabase se instancia solo cuando se llama a `_get_db()` por primera vez dentro de cada request, no al importar el módulo. Esto permite que los tests se carguen sin necesidad de tener el `.env` configurado y evita errores en el arranque si las variables no están presentes.

### Complejidad Ciclomática máxima: 10
Definido en el Plan SQA. `flake8` lo verifica con `--max-complexity=10` en cada commit. La única función que superó el umbral fue `listar_historial` (CC=11), que fue refactorizada en tres funciones auxiliares para bajarla a 6.

---

## Requerimientos

| ID | Descripción |
|----|-------------|
| REQ-F01 | Registrar, editar y eliminar repuestos (nombre, categoría, marca, serie, precio, stock) |
| REQ-F02 | Registrar entrada de stock con repuesto, cantidad, proveedor, empleado y fecha |
| REQ-F03 | Registrar salida de stock e impedir la operación si el stock resultante sería negativo |
| REQ-F04 | Consultar stock con filtros por categoría y nombre |
| REQ-F05 | Listar repuestos cuyo stock sea menor o igual al stock mínimo (stock crítico) |
| REQ-NF01 | Respuesta ≤ 2 segundos con 500+ repuestos (verificado: ~0.19s con 562 repuestos) |
| REQ-NF02 | Datos en base de datos relacional. Credenciales nunca expuestas al cliente |

---

## Estructura del proyecto

```
autobhan/
├── backend/
│   ├── main.py
│   ├── Procfile
│   ├── runtime.txt              # Fija Python 3.12 para Railway
│   ├── requirements.txt         # Dependencias de producción
│   ├── requirements-dev.txt     # Dependencias de desarrollo y testing
│   ├── routers/
│   │   ├── auth.py
│   │   ├── repuestos.py         # CRUD completo: GET, POST, PATCH, DELETE
│   │   ├── stock.py
│   │   ├── alertas.py
│   │   └── historial.py
│   ├── schemas/
│   ├── db/
│   └── tests/
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── Repuestos.jsx    # Edición inline + eliminación con confirmación
│       │   ├── Movimientos.jsx  # Selector con búsqueda predictiva
│       │   ├── Historial.jsx
│       │   └── Login.jsx
│       └── services/
│           └── api.js
└── docs/
    ├── requerimientos.md
    ├── plan_sqa.md
    ├── pipeline.md
    ├── rtm.md
    ├── plan_pruebas.md
    └── reporte_defectos.md
```

---

## Documentación

- [Catálogo de Requerimientos](docs/requerimientos.md)
- [Plan SQA](docs/plan_sqa.md)
- [Pipeline de Calidad](docs/pipeline.md)
- [Matriz de Trazabilidad (RTM)](docs/rtm.md)
- [Plan de Pruebas](docs/plan_pruebas.md)
- [Reporte de Defectos](docs/reporte_defectos.md)
