from django.db import models
from django import forms

from subastas_redes.forms.register import RegisterForm
from subastas_redes.models import Contacto


class ContactoForm(RegisterForm):
    class Meta(RegisterForm.Meta):
        model = Contacto
        fields = "__all__"
        exclude = ("date_joined", "password")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user
