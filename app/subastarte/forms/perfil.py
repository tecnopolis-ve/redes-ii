from django.db import models
from django import forms

from subastarte.forms.register import RegisterForm
from subastarte.models import Contacto

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = "__all__"
        exclude = ('date_joined', 'password', 'tienda', 'cargo', 'is_admin', 'is_active')

    fecha_nac = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#id_fecha_nac',
            'type': 'date'
        })
    )
