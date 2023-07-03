from django.db import models
from django import forms

from subastarte.models import Pintura

class PinturaForm(forms.ModelForm):

    class Meta:
        model = Pintura
        fields = "__all__"