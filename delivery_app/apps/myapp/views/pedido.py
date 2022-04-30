from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.views.generic import ListView, CreateView, DetailView

from apps.myapp.CONSTANTS import lat_a, long_a
from apps.myapp.forms.pedido import PedidoForm
from apps.myapp.mixing import Directions
from apps.myapp.models.pedido import Pedido
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from django.utils.translation import ugettext as _  # , ungettext


class PedidoListView(ListView):
    model = Pedido
    paginate_by = settings.PER_PAGE
    template_name = "myapp/pedido/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'id')
        self.f = empty(self.request, 'f', 'cliente')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = ('Seleccione %s para Cambiar') % ('menu')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class PedidoCreateView(CreateView):
    """  """
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('myapp:pedido_list')
    template_name = "myapp/pedido/form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PedidoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = _('Add %s') % _('Menu')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was added successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
        return super(PedidoCreateView, self).form_valid(form)


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = "myapp/pedido/detail.html"

    def get_context_data(self, **kwargs):
        context = super(PedidoDetailView, self).get_context_data(**kwargs)
        print(self.object)

        lat_b = self.object.geolocation.lat
        long_b = self.object.geolocation.lon
        directions = Directions(
            lat_a=lat_a,
            long_a=long_a,
            lat_b=lat_b,
            long_b=long_b
        )
        context['google_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['lat_a'] = lat_a
        context['long_a'] = long_a
        context['lat_b'] = lat_b
        context['long_b'] = long_b
        context['origin'] = f'{lat_a}, {long_a}'
        context['destination'] = f'{lat_b}, {long_b}'
        # context['origin'] = "%s,%s" % (lat_a, long_a)
        # context['destination'] ="%s,%s" % (lat_b, long_b)
        context['directions'] = directions
        return context
