# AutoBhan Autopartes — Sistema de Gestión de Inventario

Sistema web para gestión de stock de repuestos de automotores (autos, motos, camionetas).  
Proyecto integrador — Ingeniería de Software II — IUA 2026 — Grupo 6.

## Integrantes

| Nombre | Rol |
|--------|-----|
| Bubica Hundt, Mirko | QA — revisiones y estándares |
| Nuñez, Celeste Aylen | QC — testing y defectos |
| Olguin, Daniel David | Documentador + Referente |

## Stack tecnológico

- **Backend:** Python 3.11 + FastAPI + Uvicorn
- **Frontend:** React 18 + Vite
- **Base de datos:** Supabase (PostgreSQL)
- **ORM/Cliente:** supabase-py
- **Auth:** Supabase Auth (login de administrador)

## Requisitos previos

- Python 3.11+
- Node.js 18+
- Cuenta en Supabase con proyecto creado

## Instalación — Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

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
Documentación automática: `http://localhost:8000/docs`

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

## Ejecutar tests

```bash
cd backend
pytest --cov=. --cov-report=term-missing
```

## Ejecutar linter

```bash
cd backend
flake8 . --max-complexity=10
```

## Métricas de complejidad

```bash
cd backend
radon cc . -a -s    # Complejidad Ciclomática
radon mi . -s       # Maintainability Index
radon raw . -s      # Líneas de código
```

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

Respuesta `201 Created`:
```json
{
  "id": 613,
  "repuesto_id": 1,
  "tipo": "entrada",
  "cantidad": 10,
  "empleado": "Mirko Bubica",
  "fecha": "2026-06-14"
}
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
```

Respuesta `200 OK`: lista de objetos `RepuestoResponse` filtrados por categoría.

### Listar repuestos en stock crítico — REQ-F05

```bash
curl http://localhost:8000/alertas/stock-critico
```

Respuesta `200 OK`: lista de repuestos cuyo `stock_actual <= stock_minimo`.

### Login de administrador — REQ-NF02

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@autobhan.com",
    "password": "********"
  }'
```

Respuesta `200 OK`:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_email": "admin@autobhan.com"
}
```

Si las credenciales son inválidas, responde `401 Unauthorized`.

## Variables de entorno

### Backend (`backend/.env`)

| Variable | Descripción |
|----------|-------------|
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_KEY` | Anon key de Supabase |
| `APP_ENV` | `development` o `production` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS, separados por coma (URL del frontend) |

### Frontend (`frontend/.env`)

| Variable | Descripción |
|----------|-------------|
| `VITE_API_URL` | URL base del backend (FastAPI) |

> ⚠️ El frontend **nunca** debe tener credenciales de Supabase. Toda comunicación con
> Supabase pasa por el backend (REQ-NF02).

## Deploy en Railway

El proyecto se despliega como **dos servicios** dentro del mismo proyecto de Railway.

### Backend

1. **New Service → Deploy from GitHub repo** → seleccionar este repositorio
2. **Settings → Root Directory** → `backend`
3. Railway detecta Python e instala `requirements.txt` automáticamente
4. El `Procfile` ya define el comando de arranque:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Variables** → configurar `SUPABASE_URL`, `SUPABASE_KEY`, `APP_ENV=production` y `CORS_ORIGINS` (URL del frontend deployado)

### Frontend

1. **New Service → Deploy from GitHub repo** → mismo repositorio
2. **Settings → Root Directory** → `frontend`
3. **Build Command** → `npm run build`
4. **Start Command** → `npm run preview` (sirve el build con `--host 0.0.0.0 --port $PORT`)
5. **Variables** → configurar `VITE_API_URL` con la URL del backend deployado

### Orden recomendado

1. Deployar el **backend** primero (con `CORS_ORIGINS` apuntando a `localhost` temporalmente)
2. Copiar la URL pública que Railway asigna al backend
3. Deployar el **frontend**, seteando `VITE_API_URL` con esa URL
4. Copiar la URL pública del frontend
5. Volver al backend y actualizar `CORS_ORIGINS` con la URL del frontend — Railway redeploya automáticamente al cambiar variables

## Requerimientos funcionales

| ID | Descripción |
|----|-------------|
| REQ-F01 | Registrar un repuesto con nombre, categoría, marca, número de serie, precio y stock inicial |
| REQ-F02 | Registrar entrada de stock (reposición) con repuesto, cantidad, proveedor, empleado y fecha |
| REQ-F03 | Registrar salida de stock (venta/uso) e impedir operación si el stock resultante sería negativo |
| REQ-F04 | Consultar stock actual de todos los repuestos con filtros por categoría |
| REQ-F05 | Listar repuestos cuyo stock sea menor o igual al stock mínimo configurado (stock crítico) |
| REQ-NF01 | La consulta de stock no debe superar 2 segundos con hasta 500 repuestos registrados |
| REQ-NF02 | Los datos deben persistir en base de datos relacional (Supabase/PostgreSQL) |

## Estructura del proyecto

```
autobhan/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── repuestos.py
│   │   ├── stock.py
│   │   ├── alertas.py
│   │   └── historial.py
│   ├── models/
│   ├── schemas/
│   ├── db/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── Repuestos.jsx
│       │   ├── Movimientos.jsx
│       │   ├── Historial.jsx
│       │   └── Login.jsx
│       └── services/
└── docs/
    ├── requerimientos.md
    ├── plan_sqa.md
    ├── pipeline.md
    ├── rtm.md
    ├── plan_pruebas.md
    └── reporte_defectos.md
```

## Documentación

- [Catálogo de Requerimientos](docs/requerimientos.md)
- [Plan SQA](docs/plan_sqa.md)
- [Pipeline de Calidad](docs/pipeline.md)
- [Matriz de Trazabilidad (RTM)](docs/rtm.md)
- [Plan de Pruebas](docs/plan_pruebas.md)
- [Reporte de Defectos](docs/reporte_defectos.md)
