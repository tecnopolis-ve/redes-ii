from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from subastarte.models import Evento, ObjetoSubastaEvento, Tienda, Organiza
from django.utils import timezone

def list(request):
    data = Tienda.objects.all()
    return render(request, "public/organizadores/list.html", {'data': data})

def detail(request, id):
    tienda = Tienda.objects.get(pk=id)

    organiza = Organiza.objects.filter(tienda_id=tienda.pk).all()
    if organiza:
        organiza = organiza.filter(evento__fecha__gte=timezone.now().date()).all()
    return render(request, "public/organizadores/detail.html", {'tienda': tienda, 'data': organiza})