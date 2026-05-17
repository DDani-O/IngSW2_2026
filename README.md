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
pip install -r requirements.txt
cp .env.example .env            # completar con tus credenciales
uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`  
Documentación automática: `http://localhost:8000/docs`

## Instalación — Frontend

```bash
cd frontend
npm install
cp .env.example .env            # completar con URL del backend
npm run dev
```

El frontend queda disponible en `http://localhost:5173`

## Configurar pre-commit hook (obligatorio, una sola vez)

El repositorio incluye un hook que corre **flake8 y pytest automáticamente** antes de cada commit. Si alguno falla, el commit se cancela.

**Windows (PowerShell):**
```powershell
.\setup-hooks.ps1
```

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

## Variables de entorno

Ver `backend/.env.example` y `frontend/.env.example` para la lista completa de variables necesarias.

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
│   │   └── alertas.py
│   ├── models/
│   ├── schemas/
│   ├── db/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       ├── components/
│       └── services/
└── docs/
    ├── plan_sqa.md
    └── rtm.md
```

## Documentación

- [Plan SQA](docs/plan_sqa.md)
- [Matriz de Trazabilidad (RTM)](docs/rtm.md)
