"""Vistas del CRUD de productos.

Reglas de acceso (se comprueban en el servidor, en cada petición):
- Usuario anónimo: ninguna vista; LoginRequiredMixin lo redirige al login.
- Usuario autenticado: consulta, crea, edita y elimina solo SUS productos.
- Usuario con el permiso inventario.ver_todos (supervisor): además puede
  consultar (listar y ver detalle) los productos de otros, con el correo del
  proveedor enmascarado. No puede editarlos ni eliminarlos.

Los registros ajenos responden 404, no 403, para no confirmar que existen.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto

PERMISO_VER_TODOS = 'inventario.ver_todos'


class PropiosMixin(LoginRequiredMixin):
    """Limita el queryset a los productos del usuario que hace la petición."""

    def get_queryset(self):
        return Producto.objects.filter(propietario=self.request.user)


class ConsultaMixin(LoginRequiredMixin):
    """Para lectura: los propios, o todos si el usuario es supervisor."""

    def get_queryset(self):
        productos = Producto.objects.select_related('propietario')
        if self.request.user.has_perm(PERMISO_VER_TODOS):
            return productos.exclude(propietario__isnull=True)
        return productos.filter(propietario=self.request.user)


class ProductoListView(ConsultaMixin, ListView):
    model = Producto
    paginate_by = 20


class ProductoDetailView(ConsultaMixin, DetailView):
    model = Producto


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        # El propietario sale de la sesión, no de los datos enviados.
        form.instance.propietario = self.request.user
        messages.success(self.request, 'Producto creado.')
        return super().form_valid(form)


class ProductoUpdateView(PropiosMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado.')
        return super().form_valid(form)


class ProductoDeleteView(PropiosMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Producto eliminado.')
        return super().form_valid(form)
