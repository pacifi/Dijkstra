from django.db import models

from apps.myapp.models.pedido import Pedido
from apps.myapp.models.salida import Salida


class SalidaPedido(models.Model):
    salida = models.ForeignKey(Salida)
    pedido = models.ForeignKey(Pedido, blank=True, null=True)
    orden = models.IntegerField()
    lat = models.CharField(u"Latitud", max_length=50)
    long = models.CharField(u"Lingitud", max_length=50)
    literal = models.CharField(u"literal", max_length=10)
    distancia = models.CharField(u"Distancia", max_length=50)

    class Meta:
        verbose_name = "SalidaPedido"
        verbose_name_plural = "SalidaPedidos"

    def __str__(self):
        return "%s %s" % (self.salida.id, self.pedido)
