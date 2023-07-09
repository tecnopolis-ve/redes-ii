from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from subastas_redes.models import Puja, ArtistaMoneda, ArtistaPintura, Evento, ObjetoSubastaEvento, Cliente, Tienda, Participante, Moneda, Pintura
from subastas_redes.forms.puja import PujaForm
from django.db.models import Q
from functools import reduce
from django.utils import timezone
from django.contrib import messages
from itertools import chain
import operator, datetime

def list(request, subasta_id=None, tienda_id=None):

    moneda = request.GET.get('moneda', None)
    pintura = request.GET.get('pintura', None)
    precio_minimo = request.GET.get('precio_minimo', None)
    precio_maximo = request.GET.get('precio_maximo', None)

    filtros_and = []
    filtros_or = []
    or_cond = None

    if subasta_id:

        if moneda:
            filtros_or.append(Q(moneda_id__isnull=False))

        if pintura:
            filtros_or.append(Q(pintura_id__isnull=False))

        if precio_minimo:
            filtros_and.append(Q(ask__gte=precio_minimo))

        if precio_maximo:
            filtros_and.append(Q(ask__lte=precio_maximo))

        evento = Evento.objects.get(pk=subasta_id)
        objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(evento_id=evento.pk).order_by('orden').all()

        if filtros_or:
            or_cond = reduce(operator.or_, filtros_or)
            objeto_subasta_evento = objeto_subasta_evento.filter(or_cond)

        if filtros_and:
            and_cond = reduce(operator.and_, filtros_and)
            objeto_subasta_evento = objeto_subasta_evento.filter(and_cond)

        paginator = Paginator(objeto_subasta_evento, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "public/articulos/list-subasta.html", {
            'evento': evento, 
            'data': page_obj,
        })
    
    elif tienda_id:

        tienda = Tienda.objects.filter(pk=tienda_id).first()

        monedas = []
        pinturas = []

        if moneda or not (moneda or pintura):
            monedas = Moneda.objects.filter(coleccionista_id__isnull=True, tienda_id=tienda.pk)

        if pintura or not (moneda or pintura):
            pinturas = Pintura.objects.filter(coleccionista_id__isnull=True, tienda_id=tienda.pk)

        catalogo_moneda = sorted(chain(monedas, pinturas), key=lambda data: data.nur, reverse=False)

        paginator = Paginator(catalogo_moneda, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "public/articulos/list.html", {
            'tienda': tienda,
            'data': page_obj
        })

    else:

        monedas = []
        pinturas = []

        if moneda or not (moneda or pintura):
            monedas = Moneda.objects.filter(coleccionista_id__isnull=True)

        if pintura or not (moneda or pintura):
            pinturas = Pintura.objects.filter(coleccionista_id__isnull=True)

        catalogo_moneda = sorted(chain(monedas, pinturas), key=lambda data: data.nur, reverse=False)

        paginator = Paginator(catalogo_moneda, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "public/articulos/list.html", {
            'data': page_obj
        })

def detail(request, tipo, nur, subasta_id=None):
    
    render_view = None
    participante = False
    evento = None
    objeto_subasta_evento = None
    item_admite_ofertas = True
    artistas = None
    form = None

    if tipo == 'moneda':
        articulo = Moneda.objects.get(pk=nur)
        render_view = "public/articulos/mdetail.html"
        artistas = ArtistaMoneda.objects.filter(moneda=articulo.pk).all()

    else:
        articulo = Pintura.objects.get(pk=nur)
        render_view = "public/articulos/pdetail.html"
        artistas = ArtistaPintura.objects.filter(pintura=articulo.pk).all()

    if subasta_id:

        usuario_id = request.user.pk
        evento = Evento.objects.filter(pk=subasta_id, cancelado=False).get()
        objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(evento_id=evento.pk)

        if tipo == 'moneda':
            objeto_subasta_evento = objeto_subasta_evento.filter(moneda=articulo.pk).get()
        else:
            objeto_subasta_evento = objeto_subasta_evento.filter(pintura=articulo.pk).get()

        if usuario_id:
            cliente = Cliente.objects.filter(tienda_id=objeto_subasta_evento.tienda.pk).filter(coleccionista__pk=usuario_id).first()
            if cliente:
                participante = Participante.objects.filter(evento_id=evento.pk, cliente_id=cliente.pk).first()

                puja = Puja()
                puja.participante = participante
                puja.objeto_subasta_evento = objeto_subasta_evento

                form = PujaForm(instance=puja)

        if evento.fecha + datetime.timedelta(minutes=objeto_subasta_evento.duracion_minima) < timezone.now():
            item_admite_ofertas = False

        if request.method == "POST":

            form = PujaForm(data=request.POST)
            if form.is_valid():

                if objeto_subasta_evento.tipo_puja == 'DINAMICA':
                    objeto_subasta_evento.bid = form.data.get('bid')
                    objeto_subasta_evento.save()

                data = form.save()

                if data is not None:
                    messages.add_message(request, messages.SUCCESS, 'Hemos registrado tu oferta correctamente.')

                    if tipo == 'moneda':
                        obj = objeto_subasta_evento.moneda.pk
                    else:
                        obj = objeto_subasta_evento.pintura.pk

                    return redirect('public:articulos:detail_subasta', tipo, obj, evento.pk)

            else:
                messages.add_message(request, messages.WARNING, 'No hemos podido procesar tu solicitud porque contiene errores.')

    return render(request, render_view, {
        'articulo': articulo, 
        'artistas': artistas,
        'evento': evento,
        'objeto_subasta_evento': objeto_subasta_evento,
        'participante': participante,
        'item_admite_ofertas': item_admite_ofertas,
        'form': form,
    })
    