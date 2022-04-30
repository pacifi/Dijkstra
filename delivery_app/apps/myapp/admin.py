from django.contrib import admin
from django.shortcuts import redirect

from .models.pedido import Pedido, Producto
from apps.myapp.models.salida import Salida

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from .models.salida_pedido import SalidaPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
    exclude = ['atendido', 'distancia', 'distancia_numero', 'distancia_medida', ]

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/app/pedido/listar')

    def response_change(self, request, obj):
        return redirect('/app/pedido/listar')


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')


@admin.register(Producto)
class PedidoAdmin(admin.ModelAdmin):
    pass


@admin.register(SalidaPedido)
class SalidaPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'salida_id', 'orden', 'distancia')
