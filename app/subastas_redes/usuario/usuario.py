from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def index(request):
    return render(request, "usuario/usuario/index.html")

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def detail(request):
    return render(request, "usuario/usuario/detail.html", {'form': form})