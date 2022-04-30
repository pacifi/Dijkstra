from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from backend_apps.utils.forms import smtSave, btnCancel, btnReset

from ..models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ("is_active",)

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['pos'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['url'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['parent'].queryset = Menu.objects.filter(parent=None)

        self.fields['permission'].label_from_instance = lambda obj: "%s/%s" % (
            obj.content_type.app_label, obj.codename)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('title', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('parent', ),
                    css_class='col-md-4'),
                Div(Field('permission', ),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('pos', css_class='input-required input-integer mask-pint'),
                    css_class='col-md-4'),
                Div(Field('icon', ),
                    css_class='col-md-4'),
                Div(Field('url', css_class='input-required'),
                    css_class='col-md-4'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )
