from django.db import models
from django import forms
from django.utils.translation import gettext as _
from subastas_redes.models import Puja

class PujaForm(forms.ModelForm):

    class Meta:
        model = Puja
        fields = "__all__"
        widgets = {
            'participante': forms.HiddenInput(),
            'producto': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super(PujaForm, self).clean()
        bid = cleaned_data.get("bid")
        producto = cleaned_data.get("producto")

        current_max = max(producto.bid + 1, producto.ask)

        if not bid or bid < current_max:
            self.add_error('bid', _("El precio de oferta no puede ser menor a ${}".format(current_max)))