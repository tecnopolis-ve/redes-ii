from django.contrib.auth.forms import UserCreationForm
from django import forms
from subastas_redes.models import User
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = "__all__"
        exclude = ('date_joined', 'password', 'is_active')

    fecha_nac = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#id_fecha_nac',
            'type': 'date'
        })
    )