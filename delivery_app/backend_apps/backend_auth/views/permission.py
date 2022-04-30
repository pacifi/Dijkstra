from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _  # , ungettext
from django.views.generic.edit import BaseDeleteView, UpdateView, CreateView
from django.views.generic.list import ListView

from ..forms.permission import PermissionForm
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.security import SecurityKey, get_dep_objects
from backend_apps.utils.forms import empty


class PermissionDeleteView(BaseDeleteView):
    """ Elimina permission """
    model = Permission
    success_url = reverse_lazy('backend:permission_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):

        pk = key = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            d = self.get_object()
            self.recurso = '/%s/' % d.content_type.app_label
            if d.codename:
                self.recurso = '/%s/%s/' % (
                    d.content_type.app_label, d.content_type.name)
                codename_list = d.codename.split('_', 1)
                if len(codename_list) > 1:
                    self.recurso = '/%s/%s/%s/' % (
                        d.content_type.app_label, d.content_type.name,
                        codename_list[1]
                    )
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(PermissionDeleteView, self).dispatch(request, *args,
                                                          **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            # rastreando dependencias
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                            + ' "' + force_text(self.recurso) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = _('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.recurso)
            }
            if not d.id:
                messages.success(self.request, msg)
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class PermissionUpdateView(UpdateView):
    """ """
    model = Permission
    form_class = PermissionForm
    template_name = 'auths/permission/form.html'
    success_url = reverse_lazy('backend:permission_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'permission_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(PermissionUpdateView, self).dispatch(request, *args,
                                                          **kwargs)

    def get_initial(self):
        initial = super(PermissionUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        initial['app_label'] = d.content_type.app_label
        initial['controller_view'] = d.content_type.model
        codename_list = d.codename.split('_', 1)
        if len(codename_list) > 1:
            initial['action_view'] = codename_list[1]
        return initial

    def get_context_data(self, **kwargs):
        context = super(PermissionUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Change %s') % capfirst(_('permission'))
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            form.instance.codename = form.cleaned_data['codename']
            content_type, is_c_t_created = ContentType.objects.get_or_create(
                # name=form.cleaned_data['controller_view'].lower(),
                model=form.cleaned_data['controller_view'].lower(),
                app_label=form.cleaned_data['app_label'].lower(),
            )
            form.instance.content_type = content_type
            if Permission.objects.exclude(id=self.object.id).filter(
                    codename=form.cleaned_data[
                        'codename'], content_type=content_type
            ).count() > 0:
                form._errors['controller_view'] = form.error_class([
                    _(
                        u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': capfirst(_('permission')),
                        'field_label': form.cleaned_data['recurso'],
                    }
                ])

                transaction.savepoint_rollback(sid)
                return super(PermissionUpdateView, self).form_invalid(form)

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(form.cleaned_data['recurso'])
            }
            messages.success(self.request, msg)

            return super(PermissionUpdateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            return super(PermissionUpdateView, self).form_invalid(form)


class PermissionCreateView(CreateView):
    """  """
    model = Permission
    form_class = PermissionForm
    template_name = 'auths/permission/form.html'
    success_url = reverse_lazy('backend:permission_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Add %s') % capfirst(_('permission'))
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            form.instance.codename = form.cleaned_data['codename']
            content_type, is_c_t_created = ContentType.objects.get_or_create(
                # name=form.cleaned_data['controller_view'].lower(),
                model=form.cleaned_data['controller_view'].lower(),
                app_label=form.cleaned_data['app_label'].lower(),
            )
            form.instance.content_type = content_type

            if Permission.objects.filter(
                    codename=form.cleaned_data['codename'].lower(),
                    content_type=content_type).count() > 0:
                form._errors['controller_view'] = form.error_class([
                    _(u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': capfirst(_('permission')),
                        'field_label': form.cleaned_data['recurso'],
                    }
                ])
                transaction.savepoint_rollback(sid)
                return super(PermissionCreateView, self).form_invalid(form)

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(form.cleaned_data['recurso'])
            }
            if self.object.id:
                messages.success(self.request, msg)
            return super(PermissionCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            return super(PermissionCreateView, self).form_invalid(form)


class PermissionListView(ListView):
    """ """
    model = Permission
    paginate_by = settings.PER_PAGE
    template_name = 'auths/permission/list.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'content_type__app_label')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}
                                         ).order_by(self.o, 'content_type__model')

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Select %s to change') % capfirst(_('permission'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context
