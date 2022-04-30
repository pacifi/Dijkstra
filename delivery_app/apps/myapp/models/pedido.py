import requests
from django.db import models
import json
from django_google_maps import fields as map_fields

from apps.myapp.CONSTANTS import lat_a, long_a
from config import settings


class Pedido(models.Model):
    # salida = models.ForeignKey(Salida)
    address = map_fields.AddressField(u"Ciudad Referencia", max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    cliente = models.CharField(u"Cliente", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    atendido = models.BooleanField(default=False)
    distancia = models.CharField(u"Distiancia", max_length=50)
    distancia_numero = models.FloatField()
    distancia_medida = models.CharField(u"Medida", max_length=50)


    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def save(self, *args, **kwargs):
        origin = f'{lat_a},{long_a}'
        destination = f'{self.geolocation.lat},{self.geolocation.lon}'

        result = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': origin,
                'destination': destination,
                "key": settings.GOOGLE_MAPS_API_KEY
            })

        directions = result.json()
        if directions["status"] == "OK":
            route = directions["routes"][0]["legs"][0]
            origin = route["start_address"]
            destination = route["end_address"]
            distance = route["distance"]["text"]
            duration = route["duration"]["text"]
            self.distancia = distance
            self.distancia_numero = self.distancia.split()[0]
            self.distancia_medida = self.distancia.split()[1]
        super(Pedido, self).save()

    def __str__(self):
        return "%s" % self.cliente


class Producto(models.Model):
    pedido = models.ForeignKey(Pedido)
    producto = models.CharField(u"Producto", max_length=50)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = "Prodcuctos"

    def __str__(self):
        return self.producto
