from django.db import models
from django import forms

from subastarte.models import Moneda

class MonedaForm(forms.ModelForm):

    class Meta:
        model = Moneda
        fields = "__all__"