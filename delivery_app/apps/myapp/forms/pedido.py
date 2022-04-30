from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from apps.myapp.models.pedido import Pedido


from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from backend_apps.utils.forms import smtSave, btnCancel, btnReset


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude = ("created_at", "updated_at", "atendido",)
        fields = ['address', 'geolocation']
        widgets = {
            "address": map_widgets.GoogleMapsAddressWidget,
        }

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)




        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('address', css_class='input-required'),
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