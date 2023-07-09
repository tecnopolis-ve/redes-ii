from django.db import models
from django.forms import ModelForm

from subastas_redes.models import Pais

class PaisForm(ModelForm):

    class Meta:
        model = Pais
        fields = "__all__"