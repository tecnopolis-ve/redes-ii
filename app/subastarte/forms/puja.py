from django.db import models
from django import forms
from django.utils.translation import gettext as _
from subastarte.models import ObjetoSubastaEvento, Puja

class PujaForm(forms.ModelForm):

    class Meta:
        model = Puja
        fields = "__all__"
        widgets = {
            'participante': forms.HiddenInput(),
            'objeto_subasta_evento': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super(PujaForm, self).clean()
        bid = cleaned_data.get("bid")
        objeto_subasta_evento = cleaned_data.get("objeto_subasta_evento")

        current_max = max(objeto_subasta_evento.bid + 1, objeto_subasta_evento.ask)

        if not bid or bid < current_max:
            self.add_error('bid', _("El precio de oferta no puede ser menor a ${}".format(current_max)))