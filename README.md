# CRUD Inventario (Django)

CRUD de productos de inventario para la Evaluación U2 de Desarrollo Seguro.

- Python 3.13, Django 5.2 LTS
- Modelo `Producto`: nombre, categoría (opción cerrada), cantidad, correo del proveedor
- Todas las vistas requieren inicio de sesión

## Ejecutar en local

```bash
uv sync
cp .env.example .env   # y completar valores
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

## Pruebas

```bash
uv run python manage.py test
```
