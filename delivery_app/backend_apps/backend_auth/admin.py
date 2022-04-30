from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .models import Menu
from .models import User, Person

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "codename", "name", "content_type")
    search_fields = ("codename", "name", "content_type__app_label")


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # get_user_model()


class MyUserChangeForm(UserChangeForm):
    description = forms.CharField(
        label=_('Description'), required=False, initial='edit',
        widget=forms.Textarea)

    # is_staff = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta(UserChangeForm.Meta):
        model = User  # get_user_model()


class MyUserAdmin(UserAdmin):
    """ """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('email', 'person',)}),
        (_('Permissions'), {'fields': ('is_active', 'description', 'is_staff',
                                       'is_superuser', 'groups',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('username', 'email',
                    'first_name', 'last_name', 'is_staff',)  # 'status'

    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups', 'date_joined')

    # date_hierarchy = 'date_joined'

    def status(self, obj):
        return obj.status

    status.admin_order_field = 'status'
    status.short_description = 'status'

    # raw_id_fields = ('person',)



    def get_queryset(self, request):
        qs = super(MyUserAdmin, self).get_queryset(request)
        # qr = qs.with_status()  # add 'status' colum
        # print qr
        return qs


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)
    list_display = (
        'first_name', 'last_name', 'identity_type', 'identity_num',)


admin.site.register(Person, PersonAdmin)

admin.site.register(User, MyUserAdmin)
admin.site.register(ContentType)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Menu)
