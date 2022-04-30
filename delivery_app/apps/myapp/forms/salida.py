from django import forms
from ..models.salida import Salida


class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        exclude = ('id',)
