from django.db import models
from django import forms
from django.utils.translation import gettext as _
from subastarte.models import Evento, Organiza
import datetime

class EventoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.tienda_id = kwargs.pop('tienda_id') if kwargs.get('tienda_id')  else None
        super(EventoForm,self).__init__(*args,**kwargs)

    class Meta:
        model = Evento
        fields = "__all__"

    fecha = forms.SplitDateTimeField(
        initial=datetime.datetime.now,
        widget=forms.SplitDateTimeWidget(
            date_format=('%Y-%m-%d'), 
            date_attrs={
                'class': 'form-control',
                'data-target': '#id_fecha_0',
                'type': 'date'
            }, 
            time_format=('%H:%M'), 
            time_attrs={
                'class': 'form-control',
                'data-target': '#id_fecha_1',
                'type': 'time'
            }
        )
    )

    def clean(self):
        cleaned_data = super(EventoForm, self).clean()
        tipo_evento = cleaned_data.get("tipo")
        horas = cleaned_data.get("horas")
        lugar_subasta = cleaned_data.get("lugar_subasta")
        evento_id = self.instance.pk
        tienda_id = self.tienda_id
        total = Organiza.objects.filter(evento_id=evento_id).exclude(tienda_id=tienda_id).count()

        if tipo_evento != 'VIRTUAL':
            if total > 0:
                self.add_error('tipo', _("No se puede establecer un evento {} mientras existan otros organizadores activos.".format(tipo_evento)))
            if not lugar_subasta:
                self.add_error('lugar_subasta', _("El lugar de celebración para un evento {} es obligatorio.".format(tipo_evento)))

        if not (4 <= horas <= 6):
            self.add_error('horas', _("El evento debe durar entre 4 y 6 horas."))