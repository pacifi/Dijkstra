from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field

from django import forms
from django.contrib.auth.models import Group

from backend_apps.utils.forms import smtSave, btnCancel, btnReset


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('name', css_class='input-required'), css_class='col-md-12'
                )
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )
