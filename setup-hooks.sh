#!/bin/sh
# setup-hooks.sh
# Configura el pre-commit hook local.
# Cada integrante debe correr esto UNA VEZ al clonar el repo.
#
# Uso:
#   Unix/Mac:   sh setup-hooks.sh
#   Windows:    sh setup-hooks.sh  (desde Git Bash)

git config core.hooksPath .githooks
echo "✓ Pre-commit hook configurado."
echo "  Desde ahora, flake8 y pytest corren automáticamente antes de cada commit."
