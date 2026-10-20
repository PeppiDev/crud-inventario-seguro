"""Casos de validación en el servidor para el formulario de creación de Producto.

Reglas acordadas:
- cantidad: obligatoria, número entero, rango 0 a 9999 (ambos incluidos).
- categoria: obligatoria, solo uno de los valores cerrados del modelo
  (oficina, limpieza, tecnologia, alimentos).

Las pruebas envían el POST directo a la vista, sin navegador: no hay HTML
ni JavaScript que restrinja los valores, solo la validación de Django.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Producto

DATOS_VALIDOS = {
    'nombre': 'Resma carta',
    'categoria': 'oficina',
    'cantidad': '50',
    'correo_proveedor': 'ventas@proveedor.cl',
}


class ValidacionCrearProductoTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('tester', password='clave-de-prueba-123')
        self.client.force_login(user)

    def enviar(self, **cambios):
        datos = {**DATOS_VALIDOS, **cambios}
        return self.client.post(reverse('inventario:crear'), datos)

    def assertAceptado(self, respuesta):
        self.assertEqual(respuesta.status_code, 302, 'se esperaba redirección (guardado)')
        self.assertEqual(Producto.objects.count(), 1)

    def assertRechazado(self, respuesta, campo):
        self.assertEqual(respuesta.status_code, 200, 'se esperaba volver al formulario')
        self.assertIn(campo, respuesta.context['form'].errors)
        self.assertEqual(Producto.objects.count(), 0, 'no debe guardarse nada')

    # --- cantidad ---
    def test_c1_cantidad_dentro_del_rango_se_acepta(self):
        self.assertAceptado(self.enviar(cantidad='50'))

    def test_c2_cantidad_bajo_el_minimo_se_rechaza(self):
        self.assertRechazado(self.enviar(cantidad='-1'), 'cantidad')

    def test_c3a_cantidad_minimo_exacto_cero_se_acepta(self):
        self.assertAceptado(self.enviar(cantidad='0'))

    def test_c3b_cantidad_maximo_exacto_9999_se_acepta(self):
        self.assertAceptado(self.enviar(cantidad='9999'))

    def test_c3c_cantidad_sobre_el_maximo_se_rechaza(self):
        self.assertRechazado(self.enviar(cantidad='10000'), 'cantidad')

    # --- categoria ---
    def test_c4_categoria_legitima_se_acepta(self):
        self.assertAceptado(self.enviar(categoria='tecnologia'))

    def test_c5a_categoria_fuera_de_la_lista_se_rechaza(self):
        # valor manipulado que el <select> nunca ofrecería
        self.assertRechazado(self.enviar(categoria='armas'), 'categoria')

    def test_c5b_categoria_faltante_se_rechaza(self):
        self.assertRechazado(self.enviar(categoria=''), 'categoria')

    def test_c6_categoria_etiqueta_en_vez_de_valor_se_rechaza(self):
        # frontera: 'Oficina' es la etiqueta visible, no el valor guardado 'oficina'
        self.assertRechazado(self.enviar(categoria='Oficina'), 'categoria')
