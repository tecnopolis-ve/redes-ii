from django.db import models
from django.forms import ModelForm

from subastarte.models import Pais

class PaisForm(ModelForm):

    class Meta:
        model = Pais
        fields = "__all__"