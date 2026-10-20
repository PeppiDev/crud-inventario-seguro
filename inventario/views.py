from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    paginate_by = 20


class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado.')
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado.')
        return super().form_valid(form)


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('inventario:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Producto eliminado.')
        return super().form_valid(form)
