from django.db import models
from django.forms import ModelForm

from subastarte.models import Artista

class ArtistaForm(ModelForm):

    class Meta:
        model = Artista
        fields = "__all__"