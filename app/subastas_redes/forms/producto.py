from django.db import models
from django import forms

from subastas_redes.models import Producto

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = "__all__"