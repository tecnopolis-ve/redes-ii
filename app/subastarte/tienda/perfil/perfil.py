from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import Contacto
from subastarte.forms.perfil import PerfilForm
from django.contrib import messages

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request):
    perfil = Contacto.objects.get(pk=request.user.pk)
    form = PerfilForm(instance=perfil)

    if request.method == "POST":
        form = PerfilForm(data=request.POST, instance=perfil)

        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:perfil:detail')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/perfil/detail.html", {'form': form})