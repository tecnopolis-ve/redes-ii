from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from subastas_redes.models import User
from subastas_redes.forms.user import UserForm

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def index(request):
    return render(request, "usuario/usuario/index.html")

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def detail(request):
    usuario = User.objects.get(pk=request.user.pk)
    form = UserForm(instance=usuario)

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=usuario)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('usuario:detail')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "usuario/usuario/detail.html", {'form': form})