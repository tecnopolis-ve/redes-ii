from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastas_redes.models import Cliente

@login_required
@user_passes_test(lambda u:u.is_admin)
def list(request):
    data = Cliente.objects.filter(tienda_id=request.user.contacto.tienda.pk).all()
    return render(request, "tienda/clientes/list.html", {'data': data})

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request, id):
    cliente = Cliente.objects.filter(pk=id, tienda_id=request.user.contacto.tienda.pk).get()
    return render(request, "tienda/clientes/detail.html", {'cliente': cliente})