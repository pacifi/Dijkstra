from django import forms
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row
from crispy_forms.bootstrap import FormActions

from backend_apps.utils.forms import smtSave, btnCancel, btnReset


class PermissionForm(forms.ModelForm):
    """ """

    class Meta:
        model = Permission
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            label=capfirst(_(u'name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Can CRUD to Model'),
        )
        self.fields['app_label'] = forms.CharField(
            label=_(u'App'), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9_]'),
        )

        self.fields['controller_view'] = forms.CharField(
            label=_(u'Controller'), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9]'),
        )
        self.fields['action_view'] = forms.CharField(
            label=_(u'Action'), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9_]'),
        )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('app_label', css_class='input-required input-word_'),
                    css_class='col-md-4'),
                Div(Field('controller_view', css_class='input-word'),
                    css_class='col-md-4'),
                Div(Field('action_view', css_class='input-word_'),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-8'),  # input-alphanum
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )

    def clean(self):
        controller_view = self.cleaned_data['controller_view']
        action_view = self.cleaned_data['action_view']
        if not controller_view and action_view:  # TODO cambiar mensaje
            self._errors['controller_view'] = self.error_class([
                (u'Complete controlador para la accion %(action)s.') % {
                    'action': action_view}
            ])
        controller_view = self.cleaned_data['controller_view'].lower()
        app_label = self.cleaned_data['app_label'].lower()
        action_view = self.cleaned_data['action_view'].lower()

        codename = ''
        recurso = '/%s/' % app_label
        if controller_view and action_view:
            codename = '%s_%s' % (controller_view, action_view)
            recurso = '/%s/%s/%s/' % (
                app_label, controller_view, action_view)
        if controller_view and not action_view:
            codename = '%s' % (controller_view)
            recurso = '/%s/%s/' % (app_label, controller_view)

        self.cleaned_data['codename'] = codename
        self.cleaned_data['recurso'] = recurso

        return self.cleaned_data
