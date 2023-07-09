from django.db import models
from django import forms

from subastas_redes.forms.register import RegisterForm
from subastas_redes.models import Contacto

class ContactoForm(RegisterForm):

    class Meta(RegisterForm.Meta):
        model = Contacto
        fields = "__all__"
        exclude = ('date_joined', 'password')

    fecha_nac = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#id_fecha_nac',
            'type': 'date'
        })
    )
