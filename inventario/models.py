from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Producto(models.Model):
    CANTIDAD_MIN = 0
    CANTIDAD_MAX = 9999

    CATEGORIAS = [
        ('oficina', 'Oficina'),
        ('limpieza', 'Limpieza'),
        ('tecnologia', 'Tecnología'),
        ('alimentos', 'Alimentos'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    cantidad = models.IntegerField(
        validators=[MinValueValidator(CANTIDAD_MIN), MaxValueValidator(CANTIDAD_MAX)],
        help_text=f'Entre {CANTIDAD_MIN} y {CANTIDAD_MAX} unidades.',
    )
    correo_proveedor = models.EmailField()
    # Dueño del registro: lo asigna la vista al crear, nunca el formulario.
    # null=True solo para filas creadas antes de la Evaluación 3; esas filas
    # no aparecen a ningún usuario del CRUD (solo en /admin).
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, editable=False, related_name='productos',
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        permissions = [
            ('ver_todos', 'Puede consultar productos de todos los usuarios (solo lectura)'),
        ]

    def __str__(self):
        return self.nombre

    def correo_enmascarado(self):
        """Correo con la parte local oculta, p. ej. v***@proveedor.cl."""
        local, _, dominio = self.correo_proveedor.partition('@')
        return f'{local[:1]}***@{dominio}'
