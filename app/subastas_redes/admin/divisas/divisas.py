from django.urls import reverse
from django.shortcuts import render
from subastas_redes.models import Divisa
from subastas_redes.forms.divisa import DivisaForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u:u.is_superuser)
def list(request):
    data = Divisa.objects.all()
    return render(request, "admin/divisas/list.html", {'data': data})

@user_passes_test(lambda u:u.is_superuser)
def detail(request, id):
    divisa = Divisa.objects.get(pk=id)
    return render(request, "admin/divisas/detail.html", {'divisa': divisa})

@user_passes_test(lambda u:u.is_superuser)
def add(request):
    form = DivisaForm()

    if request.method == "POST":
        form = DivisaForm(data=request.POST)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:divisas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/divisas/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def edit(request, id):
    divisa = Divisa.objects.get(pk=id)
    form = DivisaForm(instance=divisa)

    if request.method == "POST":
        form = DivisaForm(data=request.POST, instance=divisa)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:divisas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/divisas/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def delete(request, id):
    divisa = Divisa.objects.get(pk=id)
    divisa.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('staff:divisas:list')