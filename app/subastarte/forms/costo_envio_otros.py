from django.db import models
from django import forms

from subastarte.models import CostoEnvioOtros

class CostoEnvioOtrosForm(forms.ModelForm):
    class Meta:
        model = CostoEnvioOtros
        fields = "__all__"