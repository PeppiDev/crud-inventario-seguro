#!/usr/bin/env bash
# Deja el laboratorio limpio: base nueva y cuentas de prueba nuevas.
# Las contraseñas quedan FUERA del repositorio, en ../.e3-cuentas-lab (chmod 600).
set -euo pipefail
cd "$(dirname "$0")/../.."
docker compose down -v
docker compose up --build -d
until curl -fs -o /dev/null http://127.0.0.1:8000/cuentas/login/; do sleep 2; done
docker compose exec -T web python manage.py crear_cuentas_prueba > ../.e3-cuentas-lab
chmod 600 ../.e3-cuentas-lab
echo "laboratorio listo; cuentas en ../.e3-cuentas-lab"
