from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import Cliente, Organiza, Participante
from subastarte.forms.coleccionista import ColeccionistaForm
from django.contrib import messages
from functools import reduce
from django.db.models import Q
from django.utils import timezone
import operator
from django.db.models import Count

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def list(request):
    tiendas_cliente = Cliente.objects.filter(coleccionista=request.user.pk).all()
    tiendas_id = tiendas_cliente.values_list('tienda_id', flat=True)
    clientes_id = tiendas_cliente.values_list('pk', flat=True)

    todos_eventos = Organiza.objects.filter(tienda_id__in=tiendas_id).distinct('evento')
    eventos = todos_eventos.filter(reduce(operator.and_, [Q(evento__cancelado=False), Q(evento__fecha__gte=timezone.now().date())]))
    historicos = todos_eventos.filter(reduce(operator.or_, [Q(evento__cancelado=True), Q(evento__fecha__lt=timezone.now().date())]))

    for organiza in eventos:
        participante = Participante.objects.filter(evento=organiza.evento.pk, cliente__in=clientes_id).first()
        if participante:
            organiza.participa = True

    return render(request, "usuario/eventos/list.html", {
        'eventos': eventos,
        'historicos': historicos
    })

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def detail(request):
    pass