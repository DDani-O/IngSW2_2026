"""
Pre-commit hook — AutoBhan Autopartes
Trazabilidad: Plan SQA — Seccion 8 (Frecuencia de medicion)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"

VENV_WIN  = BACKEND / "venv" / "Scripts" / "python.exe"
VENV_UNIX = BACKEND / "venv" / "bin" / "python"

if VENV_WIN.exists():
    PYTHON = str(VENV_WIN)
elif VENV_UNIX.exists():
    PYTHON = str(VENV_UNIX)
else:
    print("\n==========================================")
    print(" AutoBhan — Pre-commit check")
    print("==========================================")
    print("\n  No se encontro el venv en backend/venv/")
    print("  Corré: cd backend && python -m venv venv")
    print("         venv\\Scripts\\activate")
    print("         python -m pip install -r requirements.txt")
    sys.exit(1)

print("\n==========================================")
print(" AutoBhan — Pre-commit check")
print("==========================================")

print("\n [1/2] Linter (flake8)...")
r = subprocess.run(
    [PYTHON, "-m", "flake8", ".", "--max-complexity=10",
     "--exclude=venv,__pycache__"],
    cwd=BACKEND
)
if r.returncode != 0:
    print("\n COMMIT CANCELADO - El linter reporto errores.")
    sys.exit(1)
print(" Linter OK - 0 errores")

print("\n [2/2] Tests (pytest)...")
r = subprocess.run(
    [PYTHON, "-m", "pytest", "--tb=short", "-q"],
    cwd=BACKEND
)
if r.returncode != 0:
    print("\n COMMIT CANCELADO - Hay tests fallando.")
    sys.exit(1)
print(" Tests OK")

print("\n Pre-commit check completo - procediendo con el commit.")
print("==========================================\n")
sys.exit(0)
