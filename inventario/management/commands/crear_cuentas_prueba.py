"""Crea las cuentas ficticias del laboratorio con contraseñas aleatorias.

Uso: python manage.py crear_cuentas_prueba
Las contraseñas se muestran una sola vez en la consola; no se guardan en
archivos ni en el repositorio. Si la cuenta ya existe, se le asigna una nueva.
"""
import secrets

from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand

CUENTAS = [
    ('ana', False, 'operadora: CRUD de sus propios productos'),
    ('beto', False, 'operador: CRUD de sus propios productos'),
    ('sofia', True, 'supervisora: consulta todo en solo lectura'),
]


class Command(BaseCommand):
    help = 'Crea o reinicia las cuentas de prueba ana, beto y sofia.'

    def handle(self, *args, **options):
        ver_todos = Permission.objects.get(codename='ver_todos')
        for nombre, supervisor, rol in CUENTAS:
            usuario, _ = User.objects.get_or_create(username=nombre)
            clave = secrets.token_urlsafe(12)
            usuario.set_password(clave)
            usuario.save()
            if supervisor:
                usuario.user_permissions.add(ver_todos)
            self.stdout.write(f'{nombre:6} {clave}  ({rol})')
