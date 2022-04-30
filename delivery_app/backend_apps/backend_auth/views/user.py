from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import BaseDeleteView
from django.views.generic.list import ListView

from ..forms.user import UserForm
from ..models import Person
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import SecurityKey, get_dep_objects
from config import settings
from ..models import User


class UserListView(ListView):
    model = User
    template_name = "auths/user/list.html"
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'username')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = ('Seleccione %s para cambiar') % 'Usuario'

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class UserCreateView(CreateView):
    """  """
    model = User
    form_class = UserForm
    template_name = 'auths/user/form.html'
    success_url = reverse_lazy('backend:user_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):

        key = self.kwargs.get('pk', None)
        self.person_pk = None
        if key:
            self.person_pk = SecurityKey.is_valid_key(
                self.request, key, 'user_cre')
            if not self.person_pk:
                return HttpResponseRedirect(reverse_lazy('backend:user_list'))

        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = ('Agregar %s') % 'User'
        return context

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super(UserCreateView, self).get_initial()
        initial = initial.copy()

        if self.person_pk:
            d = Person.objects.get(pk=self.person_pk)
            if d:
                initial['photo'] = d.photo
                initial['first_name'] = d.first_name
                initial['last_name'] = d.last_name
                initial['identity_type'] = d.identity_type
                initial['identity_num'] = d.identity_num
                initial['person_id'] = d.pk
                # initial['password2'] = ''

        return initial

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            # raise Exception('eeee')
            try:
                person = Person.objects.get(
                    pk=self.request.POST.get("person_id"))
            except Exception as e:
                person = Person()
                person.save()
                pass
            person.first_name = form.cleaned_data['first_name']
            person.last_name = form.cleaned_data['last_name']
            person.identity_type = form.cleaned_data['identity_type']
            person.identity_num = form.cleaned_data['identity_num']
            person.photo = form.cleaned_data['photo']

            # Personalizando los mensajes de error para los Field form
            person.save()
            self.object = form.save(commit=False)
            self.object.person = person

            self.object.save()
            d = self.object

            groups = self.request.POST.getlist("groups")
            groups = list(set(groups))

            for value in groups:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            msg = ('El %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
                'name': self.model._meta.verbose_name,
                'obj': self.object
            }
            if self.object.id:
                messages.success(self.request, msg)

            return super(UserCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)

            return super(UserCreateView, self).form_invalid(form)


class UserUpdateView(UpdateView):
    """ """
    model = User
    template_name = "auths/user/form.html"
    form_class = UserForm
    success_url = reverse_lazy('backend:user_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)

        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        msg = (u'%s is not selected or not found in the database.') % (
            'Headquar')

        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = 'Change %s' % 'user'
        return context

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = self.object
        return kwargs

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        if d.person:
            initial['photo'] = d.person.photo
            initial['first_name'] = d.person.first_name
            initial['last_name'] = d.person.last_name
            initial['identity_type'] = d.person.identity_type
            initial['identity_num'] = d.person.identity_num
            # initial['password1'] = ''
            # initial['password2'] = ''

        return initial

    @transaction.atomic
    def form_valid(self, form):

        sid = transaction.savepoint()
        try:
            self.object = form.save(commit=False)
            try:
                person = Person.objects.get(pk=self.object.person.pk)
            except:
                person = Person()
                # person.save()
                pass

            person.first_name = form.cleaned_data['first_name']
            person.last_name = form.cleaned_data['last_name']
            person.identity_type = form.cleaned_data['identity_type']
            person.identity_num = form.cleaned_data['identity_num']
            person.photo = form.cleaned_data['photo']
            person.save()
            self.object.person = person

            self.object.save()
            d = self.object

            grupos_actuales = Group.objects.filter(user=d)
            print((grupos_actuales))
            for group_id in grupos_actuales:
                group = Group.objects.get(id=group_id.id)
                d.groups.remove(group)

            # agregando en UserHeadquar
            group_dist_list = self.request.POST.getlist("groups")

            group_dist_list = list(set(group_dist_list))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            msg = 'The %(name)s "%(obj)s" was changed successfully.' % {
                'name': self.model._meta.verbose_name,
                'obj': self.object
            }
            messages.success(self.request, msg)

            return super(UserUpdateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            return super(UserUpdateView, self).form_invalid(form)


class UserDeleteView(BaseDeleteView):
    """ Elimina module """
    model = User
    success_url = reverse_lazy('backend:user_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = key

        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)

            return HttpResponseRedirect(self.success_url)
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            if d.username == 'admin':
                raise Exception('Cannot delete %(name)s' % {
                    "name": self.model._meta.verbose_name
                            + ' "' + d + '"'
                })

            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, ('Cannot delete %(name)s') % {
                    "name": self.model._meta.verbose_name
                            + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = ('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': self.model._meta.verbose_name,
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
