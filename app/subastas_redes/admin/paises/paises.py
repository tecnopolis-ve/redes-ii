from django.urls import reverse
from django.shortcuts import render
from subastas_redes.models import Pais
from subastas_redes.forms.pais import PaisForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u:u.is_superuser)
def list(request):
    data = Pais.objects.all()
    return render(request, "admin/paises/list.html", {'data': data})

@user_passes_test(lambda u:u.is_superuser)
def detail(request, id):
    pais = Pais.objects.get(pk=id)
    return render(request, "admin/paises/detail.html", {'pais': pais})

@user_passes_test(lambda u:u.is_superuser)
def add(request):
    form = PaisForm()

    if request.method == "POST":
        form = PaisForm(data=request.POST)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:paises:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/paises/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def edit(request, id):
    pais = Pais.objects.get(pk=id)
    form = PaisForm(instance=pais)

    if request.method == "POST":
        form = PaisForm(data=request.POST, instance=pais)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:paises:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/paises/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def delete(request, id):
    pais = Pais.objects.get(pk=id)
    pais.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('staff:paises:list')