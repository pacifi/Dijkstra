from django.http import HttpResponse
from django.views import View
import simplejson as json
import requests

from apps.myapp.CONSTANTS import lat_a, long_a
from apps.myapp.goloso import goloso
from apps.myapp.models.pedido import Pedido
from apps.myapp.models.salida import Salida
from apps.myapp.models.salida_pedido import SalidaPedido
from backend_apps.backend_auth.models import User


class SalidaViewAddJson(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        lista_goloso = goloso(data['pedidos'], lat_origen=lat_a, long_origen=long_a)
        salida = Salida()
        print("postt")
        print(data['user_selected'])
        user = User.objects.get(username=data['user_selected'])
        salida.user = user
        salida.save()
        a = 1
        for punto in lista_goloso:
            salida_pedido = SalidaPedido()
            salida_pedido.salida = salida
            if not punto.referencia == 0:
                pedido = Pedido.objects.get(id=punto.referencia)
                salida_pedido.pedido = pedido
                pedido.atendido = True
                pedido.save()
            salida_pedido.lat = punto.lat
            salida_pedido.long = punto.long
            salida_pedido.orden = a
            salida_pedido.distancia = str(punto.distancia)
            salida_pedido.literal = str(punto.distancia)
            salida_pedido.save()
            a = a + 1
        data = {
            "data": "Suscces"
        }
        return HttpResponse(data, status=200, content_type="application/json")
