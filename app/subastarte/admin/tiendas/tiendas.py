from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from subastarte.models import Tienda
from subastarte.forms.tienda import TiendaForm
from django.contrib import messages

@user_passes_test(lambda u:u.is_superuser)
def list(request):
    data = Tienda.objects.all()
    return render(request, "admin/tiendas/list.html", {'data': data})

@user_passes_test(lambda u:u.is_superuser)
def detail(request, id):
    tienda = Tienda.objects.get(pk=id)
    return render(request, "admin/tiendas/detail.html", {'tienda': tienda})

@user_passes_test(lambda u:u.is_superuser)
def add(request):
    form = TiendaForm()

    if request.method == "POST":
        form = TiendaForm(data=request.POST)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:tiendas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/tiendas/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def edit(request, id):
    tienda = Tienda.objects.get(pk=id)
    form = TiendaForm(instance=tienda)

    if request.method == "POST":
        form = TiendaForm(data=request.POST, instance=tienda)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:tiendas:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/tiendas/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def delete(request, id):
    tienda = Tienda.objects.get(pk=id)
    tienda.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('staff:tiendas:list')