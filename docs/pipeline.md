# Pipeline de Calidad — AutoBhan Autopartes
**Grupo 6 · Ingeniería de Software II · IUA 2026**

El pipeline tiene 3 niveles que se ejecutan en distintos momentos del flujo de trabajo.

---

## Nivel 1 — Pre-commit (automático, local)

Se ejecuta automáticamente antes de cada `git commit` gracias al hook en `.githooks/`.

**Activación (una sola vez por máquina):**

```powershell
# Windows
git config core.hooksPath .githooks

# Mac / Linux
git config core.hooksPath .githooks
```

**Flujo:**

```
git commit
     │
     ▼
┌─────────────────────────────────┐
│  1. flake8                      │
│     --max-complexity=10         │
│     --max-line-length=100       │
│  Si hay errores → CANCELA       │
└─────────────────────────────────┘
     │ OK
     ▼
┌─────────────────────────────────┐
│  2. pytest                      │
│     --tb=short -q               │
│  Si falla algún test → CANCELA  │
└─────────────────────────────────┘
     │ OK
     ▼
  Commit realizado ✅
```

**Archivos involucrados:**

| Archivo | Propósito |
|---------|-----------|
| `.githooks/pre-commit` | Wrapper sh (Unix) |
| `.githooks/pre-commit.bat` | Wrapper bat (Windows) |
| `.githooks/pre-commit.py` | Lógica principal (multiplataforma) |
| `.flake8` | Configuración del linter |
| `backend/pytest.ini` | Configuración de pytest y markers |

---

## Nivel 2 — Medición de métricas (manual, antes de cada hito)

Desde la carpeta `backend/` con el venv activado:

```bash
# Complejidad Ciclomática — umbral: CC ≤ 10 por función
radon cc . -a -s --exclude "venv,__pycache__"

# Maintainability Index — umbral: MI ≥ 40 por módulo
radon mi . -s --exclude "venv,__pycache__"

# Líneas de código — objetivo: 800–3000 LOC
radon raw . -s --exclude "venv,__pycache__"

# Tests + cobertura — umbral: ≥ 60%
pytest --cov=. --cov-report=term-missing
```

---

## Nivel 3 — Code review (manual, por PR)

Checklist antes de mergear a `main`:

- [ ] El código corre sin errores
- [ ] El linter no reporta errores críticos
- [ ] Los tests pasan
- [ ] Hay tests para el código nuevo
- [ ] No hay secrets hardcodeados (API keys, passwords)
- [ ] Cada función de backend tiene `Trazabilidad: REQ-FXX` en el docstring

---

## Resultados actuales

| Paso | Herramienta | Umbral | Resultado |
|------|------------|--------|-----------|
| Linter | flake8 | 0 errores | ✅ 0 errores |
| Tests | pytest | 100% passing | ✅ 34/34 |
| Cobertura | pytest-cov | ≥ 60% | ✅ 95% |
| CC máximo | radon cc | ≤ 10 | ✅ 6 |
| MI mínimo | radon mi | ≥ 40 | ✅ 74.73 |
| LOC total | radon raw | 800–3000 | ✅ ~1709 |
