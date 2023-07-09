from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from subastas_redes.models import Tienda
from subastas_redes.forms.tienda import TiendaForm
from django.shortcuts import redirect

@login_required
@user_passes_test(lambda u:u.is_admin)
def index(request):
    return render(request, "tienda/tienda/index.html")

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request):
    tienda = Tienda.objects.get(pk=request.user.contacto.tienda.pk)
    form = TiendaForm(instance=tienda)

    if request.method == "POST":
        form = TiendaForm(data=request.POST, instance=tienda)
        if form.is_valid():
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:detail')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/tienda/detail.html", {'form': form})