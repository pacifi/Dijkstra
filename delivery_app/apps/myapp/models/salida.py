from django.db import models

from backend_apps.backend_auth.models import User


class Salida(models.Model):
    user = models.ForeignKey(User)  # encargado del pedido
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"

    def __str__(self):
        return "%s" % self.id
