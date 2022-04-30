from django.conf import settings
from django.views.generic import CreateView, ListView, DetailView

from apps.myapp.forms import salida
from apps.myapp.forms.salida import SalidaForm
from apps.myapp.mixing_waypoints import DirectionsWayPoint
from apps.myapp.models.pedido import Pedido
from apps.myapp.models.salida import Salida
from apps.myapp.models.salida_pedido import SalidaPedido


class SalidaCreateView(CreateView):
    model = Salida
    template_name = "myapp/salida/form.html"
    form_class = SalidaForm

    def get_context_data(self, **kwargs):
        context = super(SalidaCreateView, self).get_context_data(**kwargs)
        context['pedidos'] = Pedido.objects.filter(atendido=False)

        return context


class SalidaListView(ListView):
    model = Salida
    template_name = "myapp/salida/list.html"


class SalidaDetailView(DetailView):
    model = Salida
    template_name = "myapp/salida/detail.html"

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        rutas = SalidaPedido.objects.filter(salida=self.object).order_by('orden')

        for ruta in rutas:
            if (ruta.orden == 1):
                print("soy el a")
                lat_a = ruta.lat
                long_a = ruta.long

            if (ruta.orden == rutas.count()):
                print("soy el b")
                lat_b = ruta.lat
                long_b = ruta.long

            if (ruta.orden == 2 and ruta.orden != rutas.count()):
                print("soy el c")
                lat_c = ruta.lat
                long_c = ruta.long

            if (ruta.orden == 3 and ruta.orden != rutas.count()):
                print("soy el d")
                lat_d = ruta.lat
                long_d = ruta.long

            if (ruta.orden == 4 and ruta.orden != rutas.count()):
                print("soy el e")
                lat_e = ruta.lat
                long_e = ruta.long

            if (ruta.orden == 5 and ruta.orden != rutas.count()):
                print("soy el f")
                lat_f = ruta.lat
                long_f = ruta.long

            if (ruta.orden == 6 and ruta.orden != rutas.count()):
                print("soy el g")
                lat_g = ruta.lat
                long_g = ruta.long

            if (ruta.orden == 7 and ruta.orden != rutas.count()):
                print("soy el h")
                lat_h = ruta.lat
                long_h = ruta.long

            if (ruta.orden == 8 and ruta.orden != rutas.count()):
                print("soy el i")
                lat_i = ruta.lat
                long_i = ruta.long

            if (ruta.orden == 9 and ruta.orden != rutas.count()):
                print("soy el j")
                lat_j = ruta.lat
                long_j = ruta.long

            if (ruta.orden == 10 and ruta.orden != rutas.count()):
                print("soy el k")
                lat_k = ruta.lat
                long_k = ruta.long

            if (ruta.orden == 11 and ruta.orden != rutas.count()):
                print("soy el m")
                lat_m = ruta.lat
                long_m = ruta.long

            if (ruta.orden == 12 and ruta.orden != rutas.count()):
                print("soy el n")
                lat_n = ruta.lat
                long_n = ruta.long

        if (rutas.count() == 3):
            directions = DirectionsWayPoint(
                cantidad=3,
                lat_a=lat_a,
                long_a=long_a,
                lat_b=lat_b,
                long_b=long_b,
                lat_c=lat_c,
                long_c=long_c,

            )
            context = {
                "cantidad": 3,
                "google_api_key": settings.GOOGLE_MAPS_API_KEY,
                "lat_a": lat_a,
                "long_a": long_a,
                "lat_b": lat_b,
                "long_b": long_b,
                "lat_c": lat_c,
                "long_c": long_c,

                "origin": f'{lat_a}, {long_a}',
                "destination": f'{lat_b}, {long_b}',
                "directions": directions,
            }
        if (rutas.count() == 4):
            directions = DirectionsWayPoint(
                cantidad=4,
                lat_a=lat_a,
                long_a=long_a,
                lat_b=lat_b,
                long_b=long_b,
                lat_c=lat_c,
                long_c=long_c,
                lat_d=lat_d,
                long_d=long_d,

            )
            context = {
                "cantidad": 4,
                "google_api_key": settings.GOOGLE_MAPS_API_KEY,
                "lat_a": lat_a,
                "long_a": long_a,
                "lat_b": lat_b,
                "long_b": long_b,
                "lat_c": lat_c,
                "long_c": long_c,
                "lat_d": lat_d,
                "long_d": long_d,
                "origin": f'{lat_a}, {long_a}',
                "destination": f'{lat_b}, {long_b}',
                "directions": directions,
            }
        if (rutas.count() == 5):
            directions = DirectionsWayPoint(
                cantidad=5,
                lat_a=lat_a,
                long_a=long_a,
                lat_b=lat_b,
                long_b=long_b,
                lat_c=lat_c,
                long_c=long_c,
                lat_d=lat_d,
                long_d=long_d,
                lat_e=lat_e,
                long_e=long_e,
            )
            context = {
                "cantidad": 5,
                "google_api_key": settings.GOOGLE_MAPS_API_KEY,
                "lat_a": lat_a,
                "long_a": long_a,
                "lat_b": lat_b,
                "long_b": long_b,
                "lat_c": lat_c,
                "long_c": long_c,
                "lat_d": lat_d,
                "long_d": long_d,
                "lat_e": lat_e,
                "long_e": long_e,
                "origin": f'{lat_a}, {long_a}',
                "destination": f'{lat_b}, {long_b}',
                "directions": directions,
            }

        if (rutas.count() == 6):
            directions = DirectionsWayPoint(
                cantidad=6,
                lat_a=lat_a,
                long_a=long_a,
                lat_b=lat_b,
                long_b=long_b,
                lat_c=lat_c,
                long_c=long_c,
                lat_d=lat_d,
                long_d=long_d,
                lat_e=lat_e,
                long_e=long_e,
                lat_f=lat_f,
                long_f=long_f,
            )
            context = {
                "cantidad": 6,
                "google_api_key": settings.GOOGLE_MAPS_API_KEY,
                "lat_a": lat_a,
                "long_a": long_a,
                "lat_b": lat_b,
                "long_b": long_b,
                "lat_c": lat_c,
                "long_c": long_c,
                "lat_d": lat_d,
                "long_d": long_d,
                "lat_e": lat_e,
                "long_e": long_e,
                "lat_f": lat_f,
                "long_f": long_f,
                "origin": f'{lat_a}, {long_a}',
                "destination": f'{lat_b}, {long_b}',
                "directions": directions,
            }

        return context
