# setup-hooks.ps1
# Configura el pre-commit hook local en Windows (PowerShell).
# Cada integrante debe correr esto UNA VEZ al clonar el repo.
#
# Uso: .\setup-hooks.ps1

git config core.hooksPath .githooks
Write-Host "✓ Pre-commit hook configurado." -ForegroundColor Green
Write-Host "  Desde ahora, flake8 y pytest corren automaticamente antes de cada commit."
