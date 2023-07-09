from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from subastas_redes.models import Contacto
from subastas_redes.models import Tienda
from subastas_redes.forms.contacto import ContactoForm
from django.contrib import messages

@user_passes_test(lambda u:u.is_superuser)
def list(request, id):
    try:
        data = Contacto.objects.filter(tienda_id=id)
    except:
        data = None
    return render(request, "admin/contactos/list.html", {'data': data, 'tienda_id': id})

@user_passes_test(lambda u:u.is_superuser)
def detail(request, id):
    contacto = Contacto.objects.get(pk=id)
    return render(request, "admin/contactos/detail.html", {'contacto': contacto})

@user_passes_test(lambda u:u.is_superuser)
def add(request, tienda_id):

    form = ContactoForm()
    form.fields['tienda'].initial = tienda_id

    if request.method == "POST":
        form = ContactoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:tiendas:contactos', data.tienda.pk)

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/contactos/form.html", {'form': form, 'tienda_id': tienda_id})

@user_passes_test(lambda u:u.is_superuser)
def edit(request, id):
    contacto = Contacto.objects.get(pk=id)
    form = ContactoForm(instance=contacto)

    if request.method == "POST":
        form = ContactoForm(data=request.POST, instance=contacto)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:tiendas:contactos', contacto.tienda.pk)

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')
            
    return render(request, "admin/contactos/form.html", {'form': form, 'tienda_id': contacto.tienda.pk})

@user_passes_test(lambda u:u.is_superuser)
def delete(request, id):
    contacto = Contacto.objects.get(pk=id)
    contacto.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('staff:tiendas:contactos', contacto.tienda.pk)