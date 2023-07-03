from django.db import models
from django.forms import ModelForm

from subastarte.models import Divisa

class DivisaForm(ModelForm):

    class Meta:
        model = Divisa
        fields = "__all__"