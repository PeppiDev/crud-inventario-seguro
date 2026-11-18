"""Pruebas de autenticación y autorización (Evaluación 3).

Cada prueba hace la petición HTTP directa a la vista, como lo haría alguien
que escribe la URL o usa curl: no depende de que la interfaz oculte botones.
Las contraseñas se generan en cada ejecución; no hay credenciales en el código.
"""
import secrets

from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Producto

DATOS = {'nombre': 'Cloro', 'categoria': 'limpieza', 'cantidad': '5',
         'correo_proveedor': 'contacto@limpio.cl'}


def crear_usuario(nombre, **extra):
    clave = secrets.token_urlsafe(16)
    return User.objects.create_user(nombre, password=clave, **extra), clave


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.usuario, self.clave = crear_usuario('ana')

    def test_login_valido_redirige_al_inventario(self):
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': self.clave})
        self.assertRedirects(r, reverse('inventario:lista'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_invalido_se_rechaza(self):
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'incorrecta'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['form'].non_field_errors())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_por_get_no_cierra_sesion(self):
        self.client.force_login(self.usuario)
        r = self.client.get(reverse('logout'))
        self.assertEqual(r.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_sin_token_csrf_se_rechaza(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)
        r = cliente.post(reverse('logout'))
        self.assertEqual(r.status_code, 403)
        self.assertIn('_auth_user_id', cliente.session)

    def test_logout_con_token_csrf_cierra_sesion(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)
        cliente.get(reverse('inventario:lista'))  # la página entrega la cookie csrftoken
        token = cliente.cookies['csrftoken'].value
        r = cliente.post(reverse('logout'), {'csrfmiddlewaretoken': token})
        self.assertRedirects(r, reverse('login'))
        self.assertNotIn('_auth_user_id', cliente.session)
        # Después del cierre, la ruta privada vuelve a pedir login.
        r = cliente.get(reverse('inventario:lista'))
        self.assertEqual(r.status_code, 302)


class AnonimoTests(TestCase):
    def setUp(self):
        dueno, _ = crear_usuario('ana')
        self.producto = Producto.objects.create(propietario=dueno, nombre='Resma',
                                                categoria='oficina', cantidad=3,
                                                correo_proveedor='ventas@papel.cl')

    def test_rutas_privadas_redirigen_al_login(self):
        pk = self.producto.pk
        for url in [reverse('inventario:lista'), reverse('inventario:crear'),
                    reverse('inventario:detalle', args=[pk]),
                    reverse('inventario:editar', args=[pk]),
                    reverse('inventario:eliminar', args=[pk])]:
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 302)
                self.assertTrue(r['Location'].startswith(reverse('login')))

    def test_anonimo_no_puede_escribir(self):
        pk = self.producto.pk
        self.client.post(reverse('inventario:crear'), DATOS)
        self.client.post(reverse('inventario:editar', args=[pk]), {**DATOS, 'nombre': 'X'})
        self.client.post(reverse('inventario:eliminar', args=[pk]))
        self.assertEqual(Producto.objects.count(), 1)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Resma')


class PropietarioTests(TestCase):
    """Ana es dueña de un producto; Beto (otro usuario) intenta usarlo."""

    def setUp(self):
        self.ana, _ = crear_usuario('ana')
        self.beto, _ = crear_usuario('beto')
        self.de_ana = Producto.objects.create(propietario=self.ana, nombre='Resma',
                                              categoria='oficina', cantidad=3,
                                              correo_proveedor='ventas@papel.cl')
        self.client.force_login(self.beto)

    def test_lista_muestra_solo_los_propios(self):
        Producto.objects.create(propietario=self.beto, nombre='Toner', categoria='tecnologia',
                                cantidad=1, correo_proveedor='a@b.cl')
        r = self.client.get(reverse('inventario:lista'))
        self.assertContains(r, 'Toner')
        self.assertNotContains(r, 'Resma')

    def test_detalle_ajeno_404(self):
        r = self.client.get(reverse('inventario:detalle', args=[self.de_ana.pk]))
        self.assertEqual(r.status_code, 404)

    def test_editar_ajeno_404_y_sin_cambios(self):
        url = reverse('inventario:editar', args=[self.de_ana.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        r = self.client.post(url, {**DATOS, 'nombre': 'Modificado por beto'})
        self.assertEqual(r.status_code, 404)
        self.de_ana.refresh_from_db()
        self.assertEqual(self.de_ana.nombre, 'Resma')

    def test_eliminar_ajeno_404_y_sigue_existiendo(self):
        r = self.client.post(reverse('inventario:eliminar', args=[self.de_ana.pk]))
        self.assertEqual(r.status_code, 404)
        self.assertTrue(Producto.objects.filter(pk=self.de_ana.pk).exists())

    def test_crear_asigna_propietario_desde_la_sesion(self):
        # Aunque se envíe propietario=ana, el formulario no tiene ese campo.
        self.client.post(reverse('inventario:crear'), {**DATOS, 'propietario': self.ana.pk})
        self.assertEqual(Producto.objects.get(nombre='Cloro').propietario, self.beto)


class SupervisorTests(TestCase):
    """Un supervisor (permiso ver_todos) consulta todo, pero no modifica lo ajeno."""

    def setUp(self):
        ana, _ = crear_usuario('ana')
        self.supervisor, _ = crear_usuario('sofia')
        self.supervisor.user_permissions.add(Permission.objects.get(codename='ver_todos'))
        self.de_ana = Producto.objects.create(propietario=ana, nombre='Resma',
                                              categoria='oficina', cantidad=3,
                                              correo_proveedor='ventas@papel.cl')
        self.client.force_login(self.supervisor)

    def test_consulta_ajena_con_correo_enmascarado(self):
        r = self.client.get(reverse('inventario:detalle', args=[self.de_ana.pk]))
        self.assertContains(r, 'Resma')
        self.assertContains(r, 'v***@papel.cl')
        self.assertNotContains(r, 'ventas@papel.cl')

    def test_no_puede_editar_ni_eliminar_lo_ajeno(self):
        pk = self.de_ana.pk
        self.assertEqual(self.client.post(reverse('inventario:editar', args=[pk]), DATOS).status_code, 404)
        self.assertEqual(self.client.post(reverse('inventario:eliminar', args=[pk])).status_code, 404)
        self.assertTrue(Producto.objects.filter(pk=pk, nombre='Resma').exists())
