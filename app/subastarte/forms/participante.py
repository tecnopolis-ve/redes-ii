from django.db import models
from django.forms import ModelForm

from subastarte.models import Participante

class ParticipanteForm(ModelForm):

    class Meta:
        model = Participante
        fields = "__all__"