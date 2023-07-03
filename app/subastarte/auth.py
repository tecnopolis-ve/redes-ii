from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib import messages
from subastarte.forms.register import RegisterForm
from django.shortcuts import redirect

def registro(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)
                return redirect('/')

        else:
            messages.add_message(request, messages.WARNING, 'Error al iniciar sesión.')

    return render(request, "registration/register.html", {'form': form})