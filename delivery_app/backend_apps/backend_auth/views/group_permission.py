from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

from backend_apps.utils.forms import empty

from backend_apps.utils.decorators import permission_resource_required


class GroupPermissionsUpdateView(ListView):

    """ """
    model = Permission
    # grouppermissions es el controller
    template_name = 'auths/group/group_permission_form.html'
    success_url = reverse_lazy('backend:group_permissions_update')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupPermissionsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)
        # return self.model.objects.all().order_by("content_type__app_label",
        # "content_type__model")

    def get_context_data(self, **kwargs):
        try:
            group_list = Group.objects.all().order_by('-id')
            # obtener los permissions del group para mostrarlos
            privilegios = []
            for g in group_list:
                for p in g.permissions.all():
                    privilegios.append('%s-%s' % (p.id, g.id))
        except Exception as e:
            messages.error(self.request, e)

        context = super(
            GroupPermissionsUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'grouppermissions'
        context['title'] = 'Selccione %s para modificar' % ('permissions')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        context['group_list'] = group_list
        context['privilegios'] = privilegios
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            '''
            group_list = Group.objects.all().order_by('-id')
            old_privilegios_r = []
            for g in group_list:
                for p in g.permissions.all():
                    old_privilegios_r.append('%s-%s' % (p.id, g.id))
            '''
            old_privilegios_r = request.POST.get('old_privilegios')
            if old_privilegios_r:
                old_privilegios_r = old_privilegios_r.split(',')

            # Elimino los antiguos privilegios
            for value in old_privilegios_r:
                # el formato es 1-4 = recurso_id-perfil_id
                data = value.split('-')
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.remove(recur)

            privilegios_r = request.POST.getlist('privilegios')
            for value in privilegios_r:
                # el formato es 1-4 = recurso_id-perfil_id
                data = value.split('-')
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.add(recur)
            msg = 'El %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
                'name': '',
                'obj': 'permissions'
            }
            messages.success(self.request, msg)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            messages.error(self.request, e)

        return HttpResponseRedirect(self.success_url)
