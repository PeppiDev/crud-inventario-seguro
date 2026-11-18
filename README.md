# CRUD Inventario (Django) — Desarrollo Seguro

CRUD de productos de inventario con login y permisos por usuario.
Evaluación 2 (validación en servidor, SonarQube) y Evaluación 3 (login,
Docker y OWASP ZAP).

- Python 3.13, Django 5.2 LTS, gunicorn + WhiteNoise, SQLite
- Modelo `Producto`: nombre, categoría (opción cerrada), cantidad (0–9999),
  correo del proveedor y propietario

## Reglas de acceso

| Usuario | Puede |
|---|---|
| Anónimo | Solo ver el login. Toda otra ruta redirige a `/cuentas/login/`. |
| Operador (`ana`, `beto`) | Listar, ver, crear, editar y eliminar **sus** productos. Un producto ajeno responde 404. |
| Supervisor (`sofia`, permiso `inventario.ver_todos`) | Además, consultar los productos de todos, con el correo del proveedor enmascarado. No edita ni elimina lo ajeno. |
| Superusuario | Administración en `/admin/`. |

El cierre de sesión solo acepta POST con token CSRF.

## Laboratorio con Docker Compose

Requisitos: Docker Engine o Docker Desktop con Compose v2 (probado con
Docker Compose 5.4 sobre Podman 5.8).

```bash
# 1. Variables de entorno (no se suben al repositorio)
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(50))"   # pegar en DJANGO_SECRET_KEY

# 2. Construir y levantar (las migraciones se aplican al iniciar el contenedor)
docker compose up --build -d
docker compose ps            # estado Up; el healthcheck pasa a "healthy" a los ~30 s

# 3. Cuentas de prueba (las contraseñas aparecen una sola vez en pantalla)
docker compose exec web python manage.py crear_cuentas_prueba
docker compose exec web python manage.py createsuperuser   # opcional, para /admin/
```

Abrir <http://127.0.0.1:8000>. El puerto se publica solo en 127.0.0.1, así
que no es accesible desde otros equipos de la red.

Otros comandos:

```bash
docker compose exec web python manage.py migrate            # migraciones manuales
docker compose exec web python manage.py check --deploy     # revisión de configuración
docker compose logs -f web
docker compose down          # detener (los datos quedan en el volumen sqlite_data)
docker compose down -v       # detener y borrar la base de prueba
```

El perfil de laboratorio usa `DEBUG=False`, `ALLOWED_HOSTS=localhost,127.0.0.1`
y `DJANGO_HTTPS=False` (el laboratorio es HTTP local; en producción con HTTPS
se deja en `True` y las cookies llevan `Secure`).

## Pruebas

```bash
uv sync
cp .env.example .env    # si no existe; completar DJANGO_SECRET_KEY
uv run python manage.py test
```

O dentro del contenedor: `docker compose exec web python manage.py test`.

## Análisis de seguridad

- SonarQube: `sonar-project.properties` (las exclusiones son solo técnicas).
- OWASP ZAP: apuntar a `http://127.0.0.1:8000` y explorar con una cuenta de
  prueba. Usar solo datos ficticios; no escanear despliegues públicos.

## Ejecutar sin Docker

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py crear_cuentas_prueba
uv run python manage.py runserver
```

## Evaluación 3

Informe por secciones, evidencia y reportes ZAP en `docs/eval3/`. Scripts del laboratorio (recorrido ZAP, extracción de evidencia, capturas) en `scripts/lab/`. El PDF se genera con `uv run --with playwright --with markdown python docs/eval3/generar_pdf.py`.
