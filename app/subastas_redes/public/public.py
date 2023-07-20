from django.shortcuts import render
from subastas_redes.models import Factura, ItemFactura, Puja
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from datetime import timedelta
from django.db.models import Max

def index(request):

    return render(request, "public/public/index.html")

def procesar(request):
    pass

    messages.add_message(request, messages.SUCCESS, 'Procesado')
    return redirect('/')