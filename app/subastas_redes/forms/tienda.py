from django.db import models
from django import forms

from subastas_redes.models import Tienda

class TiendaForm(forms.ModelForm):

    class Meta:
        model = Tienda
        fields = "__all__"

    fundacion = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#id_fundacion',
            'type': 'date'
        })
    )