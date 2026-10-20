from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CrudProductoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='clave-de-prueba-123')
        self.client.force_login(self.user)
        self.producto = Producto.objects.create(
            nombre='Resma carta', categoria='oficina', cantidad=10,
            correo_proveedor='ventas@proveedor.cl',
        )

    def test_listar_requiere_login(self):
        self.client.logout()
        respuesta = self.client.get(reverse('inventario:lista'))
        self.assertEqual(respuesta.status_code, 302)

    def test_listar(self):
        respuesta = self.client.get(reverse('inventario:lista'))
        self.assertContains(respuesta, 'Resma carta')

    def test_crear(self):
        self.client.post(reverse('inventario:crear'), {
            'nombre': 'Cloro', 'categoria': 'limpieza', 'cantidad': 5,
            'correo_proveedor': 'contacto@limpio.cl',
        })
        self.assertTrue(Producto.objects.filter(nombre='Cloro').exists())

    def test_editar(self):
        self.client.post(reverse('inventario:editar', args=[self.producto.pk]), {
            'nombre': 'Resma oficio', 'categoria': 'oficina', 'cantidad': 8,
            'correo_proveedor': 'ventas@proveedor.cl',
        })
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Resma oficio')

    def test_eliminar(self):
        self.client.post(reverse('inventario:eliminar', args=[self.producto.pk]))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
