from django.db import models
from django.forms import ModelForm

from subastarte.models import ArtistaPintura

class ArtistaPinturaForm(ModelForm):

    class Meta:
        model = ArtistaPintura
        fields = "__all__"