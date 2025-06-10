from django.contrib import admin
from .models import Producto, MensajeContacto, Compra, CompraItem

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre',)
    list_editable = ('stock',)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_envio', 'mensaje')
    search_fields = ('nombre', 'email', 'asunto')
    list_filter = ('fecha_envio',)

class CompraItemInline(admin.TabularInline):
    model = CompraItem
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'email', 'orden', 'fecha', 'total', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('orden', 'usuario__username', 'email')
    inlines = [CompraItemInline]
    readonly_fields = ('usuario', 'email', 'orden', 'fecha', 'total', 'estado')