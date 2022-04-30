from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import BaseDeleteView
from django.utils.encoding import force_text
from ..forms.group import GroupForm
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects
from config import settings


class GroupListView(ListView):
    model = Group
    paginate_by = settings.PER_PAGE
    template_name = "auths/group/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'grupo'
        context['title'] = ('Seleccione %s para Cambiar') % ('Grupo')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class GroupCretaView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "auths/group/form.html"
    success_url = reverse_lazy("backend:group_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupCretaView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupCretaView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'grupo'
        context['title'] = "Agregar Menu"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'El %(name)s "%(obj)s" fue agregado satisfactoriamente' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        if self.object.id:
            messages.success(self.request, msg)
        return super(GroupCretaView, self).form_valid(form)


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "auths/group/form.html"
    success_url = reverse_lazy("backend:group_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(GroupUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'grupo'
        context['title'] = "Cambiar %s" % "Grupo"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'El %(name)s "%(obj)s" fue cambiado satisfactoriamente' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(GroupUpdateView, self).form_valid(form)


class GroupDeleteView(BaseDeleteView):
    model = Group
    success_url = reverse_lazy("backend:group_list")

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(GroupDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, ('No se puede eliminar %(name)s') % {
                    "name": self.model._meta.verbose_name + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = 'The %(name)s "%(obj)s" was deleted successfully.' % {
                'name': self.model._meta.verbose_name,
                'obj': d
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
