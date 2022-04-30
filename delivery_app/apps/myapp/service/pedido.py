from django.core import serializers
from django.http import HttpResponse
from django.views import View

from apps.myapp.models.pedido import Pedido
import simplejson as json


class PedidoViewJson(View):
    def get(self, *args, **kwargs):
        pedidos = Pedido.objects.filter(atendido=False)
        tmpJson = serializers.serialize("json", pedidos)
        tmpObj = json.loads(tmpJson)
        dump = json.dumps(tmpObj)
        return HttpResponse(dump, status=200, content_type="application/json")
