# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Implementacion de los formularios de la app sad
"""
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Row, HTML, Field
from django import forms
from django.contrib.auth.models import Group
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext_lazy as _

from ..models import Person, User, IDENTITY_TYPE_CHOICES
from backend_apps.utils.forms import btnCancel, smtSave, btnReset


class UserForm(forms.ModelForm):
    """ """
    person_id = forms.CharField(widget=forms.HiddenInput(), required=False, )
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    # no funciona para el inser por person esto está validado en el Model como
    # debe de ser ????
    def clean_identity_numxx(self):
        identity_num = self.cleaned_data['identity_num']
        identity_type = self.cleaned_data['identity_type']

        if Person.objects.exclude(id=self.instance.person.id).filter(identity_type=self.instance.person.identity_type,
                                                                     identity_num=self.instance.person.identity_num).count() > 0:
            raise forms.ValidationError(
                _(u'%(model_name)s with this %(field_label)s already exists.xxx') % {
                    'model_name': capfirst(_('Person')),
                    'field_label': get_text_list((capfirst(_('number')), capfirst(_('Type'))), _('and')),
                })
        return identity_num

    def save(self, commit=True):
        ''' # así no funciona
        if Person.objects.exclude(id=self.instance.person.id).filter(identity_type=self.instance.person.identity_type, identity_num=self.instance.person.identity_num).count() > 0:

            raise forms.ValidationError({
                'identity_num':
                (_(u'%(model_name)s with this %(field_label)s already exists.xxx pp') % {
                'model_name': _('Person'),
                'field_label': get_text_list((capfirst(_('number')), capfirst(_('Type'))), _('and')),
                },),
            })
        '''
        user = super(UserForm, self).save(commit=False)

        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', ]
        '''
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not uniquexxx.",
            }
        }
        '''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(UserForm, self).__init__(*args, **kwargs)
        # print self.request.user
        # self.fields['hidden_field'] = forms.CharField(widget=forms.HiddenInput())
        # print self.hidden_field

        self.fields['password1'] = forms.CharField(
            label=capfirst(_(u'Password')), required=False,
            widget=forms.PasswordInput, initial='',
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['password2'] = forms.CharField(
            label=capfirst(_(u'Password confirmation')), required=False,
            widget=forms.PasswordInput, initial='',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Enter the same password as above, for verification.'),
        )
        groups_final = {}
        self.fields['groups'] = forms.ModelMultipleChoiceField(
            label=u'%s %s' % (capfirst(_(u'groups')), capfirst(_(u'Roles'))), required=False,
            queryset=Group.objects.all(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        if self.object:
            self.fields['groups'].initial = [(e) for e in Group.objects.filter(
                user=self.object)]

        self.fields['first_name'] = forms.CharField(
            label=capfirst(_(u'first name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['last_name'] = forms.CharField(
            label=capfirst(_(u'last name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'] = forms.ChoiceField(
            label=capfirst(_(u'Identity type')), required=True,
            # widget=forms.RadioSelect(),
            choices=IDENTITY_TYPE_CHOICES,

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_num'] = forms.CharField(
            label=capfirst(_(u'number')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['photo'] = forms.ImageField(
            label=capfirst(_(u'Photo')), required=False,
            initial='persons/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('person_id', ),
            Row(
                Div(Field('first_name', ), css_class='col-md-6'),
                Div(Field('last_name', ), css_class='col-md-6'),
            ),
            Row(
                Div(Field('identity_type', ), css_class='col-md-6'),
                Div(Field('identity_num', ), css_class='col-md-6'),
            ),
            Row(
                Div(Field('username', autofocus=True, autocomplete='off',
                          css_class='input-required'), css_class='col-md-6'),
                Div(Field('email', ), css_class='col-md-6'),
            ),
            Row(
                Div(Field('password1', autocomplete='off'), css_class='col-md-6'),
                Div(Field('password2', autocomplete='off'), css_class='col-md-6'),
            ),
            Row(
                Div(Field('groups'), css_class='col-md-12'),
            ),
            Row(
                Div(Field('photo'), css_class='col-md-6'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )
