from django.db import models
from django import forms

from subastarte.models import Organiza

class OrganizaForm(forms.ModelForm):
    class Meta:
        model = Organiza
        fields = "__all__"
