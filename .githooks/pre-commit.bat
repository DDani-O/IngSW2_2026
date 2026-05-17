@echo off
:: Pre-commit hook para Windows — AutoBhan Autopartes
:: Trazabilidad: Plan SQA — Seccion 8

set ROOT=%~dp0..\
set BACKEND=%ROOT%backend
set PYTHON=%BACKEND%\venv\Scripts\python.exe

echo.
echo ==========================================
echo  AutoBhan -- Pre-commit check
echo ==========================================

if not exist "%PYTHON%" (
    echo.
    echo   No se encontro el venv en backend\venv\
    echo   Corré: cd backend
    echo          python -m venv venv
    echo          venv\Scripts\activate
    echo          python -m pip install -r requirements.txt
    echo.
    exit /b 1
)

echo.
echo  [1/2] Linter (flake8^)...
cd /d "%BACKEND%"
"%PYTHON%" -m flake8 . --max-complexity=10 --exclude=venv,__pycache__
if %ERRORLEVEL% neq 0 (
    echo.
    echo  COMMIT CANCELADO - El linter reporto errores.
    echo  Corregi los errores antes de commitear.
    echo.
    exit /b 1
)
echo  Linter OK - 0 errores

echo.
echo  [2/2] Tests (pytest^)...
"%PYTHON%" -m pytest --tb=short -q
if %ERRORLEVEL% neq 0 (
    echo.
    echo  COMMIT CANCELADO - Hay tests fallando.
    echo  Todos los tests deben pasar antes de commitear.
    echo.
    exit /b 1
)
echo  Tests OK

echo.
echo  Pre-commit check completo - procediendo con el commit.
echo ==========================================
echo.
exit /b 0
