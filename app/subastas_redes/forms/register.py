from django.contrib.auth.forms import UserCreationForm
from django import forms
from subastas_redes.models import User
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = "__all__"
        exclude = ('date_joined', 'password', 'is_active')
