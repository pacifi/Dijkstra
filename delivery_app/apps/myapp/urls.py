from django.conf.urls import url

from apps.myapp.service.pedido import PedidoViewJson
from apps.myapp.service.salida import SalidaViewAddJson
from apps.myapp.service.user import UserViewJson
from apps.myapp.views.pedido import PedidoListView, PedidoCreateView, PedidoDetailView
from apps.myapp.views.salida import SalidaCreateView, SalidaListView, SalidaDetailView

urlpatterns = [
    url(r'^pedido/listar$', PedidoListView.as_view(), name='pedido_list'),
    url(r'^pedido/crear$', PedidoCreateView.as_view(), name='pedido_add'),
    url(r'^pedido/detallar/(?P<pk>[^/]+)$', PedidoDetailView.as_view(), name='pedido_detail'),

    url(r'^salida/crear$', SalidaCreateView.as_view(), name='salida_add'),
    url(r'^salida/listar$', SalidaListView.as_view(), name='salida_list'),  # Menu
    url(r'^salida/detallar/((?P<pk>[0-9]+)/?$)$', SalidaDetailView.as_view(), name='salida_detail'),

    # Json
    url(r'^pedido/service_list$', PedidoViewJson.as_view(), name='pedido_service_list'),
    url(r'^user/service_list$', UserViewJson.as_view(), name='user_service_list'),
    url(r'^salida/service_add$', SalidaViewAddJson.as_view(), name='salida_service_list'),

]
