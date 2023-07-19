from django.db import models
from django import forms

from subastas_redes.forms.register import RegisterForm
from subastas_redes.models import Contacto

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = "__all__"
        exclude = ('date_joined', 'password', 'tienda', 'cargo', 'is_admin', 'is_active')
