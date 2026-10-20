#!/bin/bash
# Despliegue del CRUD en PythonAnywhere: dependencias, migraciones, estáticos, chequeos y pruebas.
# Lo ejecuta una tarea programada; la salida queda en ~/crud-inventario/logs/deploy.log
cd "$HOME/crud-inventario" || exit 1
mkdir -p logs
source "$HOME/.virtualenvs/crud/bin/activate"
{
  echo "===== Despliegue $(date -u '+%Y-%m-%d %H:%M:%S UTC') ====="
  echo '$ python --version'; python --version
  echo '$ pip install -r requirements.txt'; pip install -q -r requirements.txt && echo OK
  echo '$ pip check'; pip check
  echo '$ python manage.py migrate --noinput'; python manage.py migrate --noinput
  echo '$ python manage.py collectstatic --noinput'; python manage.py collectstatic --noinput | tail -1
  echo '$ python manage.py check --deploy'; python manage.py check --deploy 2>&1
  echo '$ python manage.py test'; python manage.py test 2>&1 | tail -4
  echo "===== Fin $(date -u '+%H:%M:%S UTC') ====="
} >> logs/deploy.log 2>&1
