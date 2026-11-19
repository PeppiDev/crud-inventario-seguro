"""Pruebas de las correcciones motivadas por ZAP (Evaluación 3)."""
import secrets

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CabecerasTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('ana', password=secrets.token_urlsafe(16))
        self.producto = Producto.objects.create(propietario=self.usuario, nombre='Resma',
                                                categoria='oficina', cantidad=3,
                                                correo_proveedor='ventas@papel.cl')

    def test_csp_estricta_en_login_y_crud(self):
        self.client.force_login(self.usuario)
        for url in [reverse('login'), reverse('inventario:lista'),
                    reverse('inventario:detalle', args=[self.producto.pk])]:
            with self.subTest(url=url):
                csp = self.client.get(url)['Content-Security-Policy']
                self.assertIn("default-src 'self'", csp)
                self.assertIn("frame-ancestors 'none'", csp)
                self.assertNotIn('unsafe-inline', csp)

    def test_html_sin_estilos_ni_scripts_inline(self):
        # Con la CSP estricta, un <style> o style="" inline dejaría de aplicarse.
        html = self.client.get(reverse('login')).content.decode()
        self.assertNotIn('<style', html)
        self.assertNotIn('style="', html)
        self.assertNotIn('<script', html)
        self.assertIn('css/app.css', html)

    def test_paginas_privadas_no_se_guardan_en_cache(self):
        self.client.force_login(self.usuario)
        for url in [reverse('inventario:lista'), reverse('inventario:crear'),
                    reverse('inventario:detalle', args=[self.producto.pk]),
                    reverse('inventario:editar', args=[self.producto.pk])]:
            with self.subTest(url=url):
                self.assertIn('no-store', self.client.get(url)['Cache-Control'])

    def test_cookie_csrftoken_httponly(self):
        r = self.client.get(reverse('login'))
        self.assertTrue(r.cookies['csrftoken']['httponly'])

    def test_sesion_dura_una_jornada(self):
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'x'})
        self.assertEqual(r.status_code, 200)  # inválido: sin cookie de sesión
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.session.get_expiry_age(), 8 * 60 * 60)


class EstaticosTests(TestCase):
    def test_css_sin_cors_abierto(self):
        from whitenoise.middleware import WhiteNoiseMiddleware
        from django.conf import settings
        self.assertFalse(settings.WHITENOISE_ALLOW_ALL_ORIGINS)
        self.assertFalse(WhiteNoiseMiddleware(lambda r: None).allow_all_origins)
