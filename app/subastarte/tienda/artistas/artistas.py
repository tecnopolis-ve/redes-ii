from django.http.request import validate_host
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import Artista
from subastarte.forms.artista import ArtistaForm
from subastarte.forms.organiza import OrganizaForm
from subastarte.forms.costo_envio_otros import CostoEnvioOtrosForm
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request, id):
    artista = Artista.objects.get(pk=id)
    return render(request, "tienda/artistas/detail.html", {'artista' : artista})

@login_required
@user_passes_test(lambda u:u.is_admin)
def list(request):
    data = Artista.objects.all()
    return render(request, "tienda/artistas/list.html", {'data' : data})

@login_required
@user_passes_test(lambda u:u.is_admin)
def add(request):
    form = ArtistaForm()

    if request.method == "POST":
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:artistas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/artistas/form.html", {'form' : form})

@login_required
@user_passes_test(lambda u:u.is_admin)
def edit(request, id):
    artista = Artista.objects.get(pk=id)
    form = ArtistaForm(instance=artista)

    if request.method == "POST":
        form = ArtistaForm(request.POST, request.FILES, instance=artista)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:artistas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/artistas/form.html", {'form' : form})

@login_required
@user_passes_test(lambda u:u.is_admin)
def delete(request, id):
    artista = Artista.objects.get(pk=id)
    artista.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('tienda:artistas:list')