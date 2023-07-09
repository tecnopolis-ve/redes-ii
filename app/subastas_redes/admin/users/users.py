from django.urls import reverse
from django.shortcuts import render
from subastas_redes.models import User
from subastas_redes.forms.user import UserForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u:u.is_superuser)
def list(request):
    data = User.objects.filter(is_admin=False).all()
    return render(request, "admin/users/list.html", {'data': data})

@user_passes_test(lambda u:u.is_superuser)
def detail(request, id):
    user = User.objects.filter(is_admin=False).get(pk=id)
    return render(request, "admin/users/detail.html", {'user': user})

@user_passes_test(lambda u:u.is_superuser)
def add(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            data = form.save()
            
            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:users:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/users/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def edit(request, id):
    user = User.objects.filter(is_admin=False).get(pk=id)
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('staff:users:list')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "admin/users/form.html", {'form': form})

@user_passes_test(lambda u:u.is_superuser)
def delete(request, id):
    user = User.objects.filter(is_admin=False).get(pk=id)
    user.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('staff:users:list')