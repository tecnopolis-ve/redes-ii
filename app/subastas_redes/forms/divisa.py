from django.db import models
from django.forms import ModelForm

from subastas_redes.models import Divisa

class DivisaForm(ModelForm):

    class Meta:
        model = Divisa
        fields = "__all__"