from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'cantidad', 'propietario']
    list_filter = ['categoria']
    search_fields = ['nombre']
    readonly_fields = ['propietario']
