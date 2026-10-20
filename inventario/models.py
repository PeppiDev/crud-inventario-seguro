from django.db import models


class Producto(models.Model):
    CATEGORIAS = [
        ('oficina', 'Oficina'),
        ('limpieza', 'Limpieza'),
        ('tecnologia', 'Tecnología'),
        ('alimentos', 'Alimentos'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    cantidad = models.IntegerField()
    correo_proveedor = models.EmailField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
