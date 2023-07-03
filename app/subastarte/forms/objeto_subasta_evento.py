from django.db import models
from django import forms

from subastarte.models import ObjetoSubastaEvento

class ObjetoSubastaEventoForm(forms.ModelForm):
    class Meta:
        model = ObjetoSubastaEvento
        fields = "__all__"