# Imagen oficial de Python, misma versión menor que el proyecto (3.13).
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Primero solo las dependencias, para aprovechar la caché de capas.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Usuario sin privilegios; /data guarda la base SQLite (volumen).
RUN useradd --uid 10001 --create-home app \
    && mkdir -p /data /app/staticfiles \
    && chown app:app /data /app/staticfiles
USER app

EXPOSE 8000

# migrate y collectstatic al iniciar: necesitan la SECRET_KEY, que solo existe en tiempo de ejecución.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput -v 0 && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile -"]
