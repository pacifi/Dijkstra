from django.views.generic.list import ListView

from django.utils.translation import ugettext as _  # , ungettext
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects
from backend_apps.utils.decorators import permission_resource_required


# models
from ..models import Menu

# forms
from ..forms.menu import MenuForm


class MenuListView(ListView):
    model = Menu
    paginate_by = settings.PER_PAGE
    template_name = "auths/menu/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'pos')
        self.f = empty(self.request, 'f', 'title')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = ('Seleccione %s para Cambiar') % ('menu')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class MenuCreateView(generic.edit.CreateView):
    """  """
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('backend:menu_list')
    template_name = "auths/menu/form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
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
        return super(MenuCreateView, self).form_valid(form)


class MenuUpdateView(generic.edit.UpdateView):
    """ """
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('backend:menu_list')
    template_name = "auths/menu/form.html"

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

        return super(MenuUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = _('Change %s') % _('Menu')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)

        return super(MenuUpdateView, self).form_valid(form)


class MenuUpdateActiveView(generic.View):
    """ """
    model = Menu
    success_url = reverse_lazy('backend:menu_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        state = self.kwargs['state']
        pk = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.success_url)
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)

        msg = _('The %(name)s "%(obj)s" was %(action)s successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('reactivated') if state == 'rea' else _('inactivated'))
        }
        mse = _('The %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('active') if state == 'rea' else _('inactive'))
        }
        try:
            if state == 'ina' and not self.object.is_active:
                raise Exception(mse)
            else:
                if state == 'rea' and self.object.is_active:
                    raise Exception(mse)
                else:
                    self.object.is_active = (True if state == 'rea' else False)
                    self.object.save()
                    messages.success(self.request, msg)
        except Exception as e:
            messages.error(self.request, e)
        return HttpResponseRedirect(self.success_url)


class MenuDeleteView(generic.edit.BaseDeleteView):
    """ Elimina module """
    model = Menu
    success_url = reverse_lazy('backend:menu_list')

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
        return super(MenuDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            print("d:", d)
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = _('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
