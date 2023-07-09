from django.http.request import validate_host
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastas_redes.models import (
    Evento,
    Organiza,
    Tienda,
    ObjetoSubastaEvento,
    CostoEnvioOtros,
    Puja,
    Moneda,
    Pintura,
)
from subastas_redes.forms.evento import EventoForm
from subastas_redes.forms.organiza import OrganizaForm
from subastas_redes.forms.costo_envio_otros import CostoEnvioOtrosForm
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from itertools import chain
import operator, datetime
from django.db.models import Q
from functools import reduce
import requests
import json
from django.http import HttpResponse


def __contar_pujas(evento_id):
    return Puja.objects.filter(objeto_subasta_evento__evento_id=evento_id).count()


@login_required
@user_passes_test(lambda u: u.is_admin)
def detail(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.get(pk=organiza_id, tienda_id=tienda_id)
    costo_envio = CostoEnvioOtros.objects.filter(evento_id=organiza.evento.pk).first()
    return render(
        request,
        "tienda/eventos/detail.html",
        {"organiza": organiza, "costo_envio": costo_envio},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def list(request):
    tienda_id = request.user.contacto.tienda.pk
    data = Organiza.objects.filter(tienda_id=tienda_id).all()
    return render(request, "tienda/eventos/list.html", {"data": data})


@login_required
@user_passes_test(lambda u: u.is_admin)
def add(request):
    tienda_id = request.user.contacto.tienda.pk
    form = EventoForm()
    costo_envio_form = CostoEnvioOtrosForm()

    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        costo_envio_form = CostoEnvioOtrosForm(request.POST, request.FILES)
        if form.is_valid() and costo_envio_form.is_valid():
            data = form.save()

            organiza = Organiza()
            organiza.evento = data
            organiza.tienda_id = tienda_id
            organiza.save()

            costo_envio_form = costo_envio_form.save(False)
            costo_envio_form.evento = data
            costo_envio_form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, "Cambios guardados.")
                return redirect("tienda:eventos:list")

        else:
            messages.add_message(
                request, messages.WARNING, "Existen errores en el formulario."
            )

    return render(
        request,
        "tienda/eventos/form.html",
        {"form": form, "costo_envio_form": costo_envio_form},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def edit(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.filter(pk=organiza_id).get()

    if __contar_pujas(organiza.evento.pk):
        messages.add_message(
            request,
            messages.WARNING,
            "No se puede modificar un evento que tenga transacciones registradas.",
        )
        return redirect("tienda:eventos:list")

    costo_envio = CostoEnvioOtros.objects.filter(evento_id=organiza.evento.pk).first()
    form = EventoForm(instance=organiza.evento, tienda_id=tienda_id)
    costo_envio_form = CostoEnvioOtrosForm(instance=costo_envio)

    if request.method == "POST":
        form = EventoForm(
            request.POST, request.FILES, instance=organiza.evento, tienda_id=tienda_id
        )
        costo_envio_form = CostoEnvioOtrosForm(
            request.POST, request.FILES, instance=costo_envio
        )
        if form.is_valid() and costo_envio_form.is_valid():
            data = form.save()

            costo_envio_form = costo_envio_form.save(False)
            costo_envio_form.evento = data
            costo_envio_form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, "Cambios guardados.")
                return redirect("tienda:eventos:list")

        else:
            messages.add_message(
                request, messages.WARNING, "Existen errores en el formulario."
            )

    return render(
        request,
        "tienda/eventos/form.html",
        {"form": form, "costo_envio_form": costo_envio_form},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def delete(request, organiza_id):
    organiza = Organiza.objects.get(pk=organiza_id)

    if __contar_pujas(organiza.evento.pk):
        messages.add_message(
            request,
            messages.WARNING,
            "No se puede modificar un evento que tenga transacciones registradas.",
        )
        return redirect("tienda:eventos:list")

    organiza.evento.delete()
    messages.add_message(
        request, messages.SUCCESS, "Registro {} eliminado.".format(organiza_id)
    )
    return redirect("tienda:eventos:list")


@login_required
@user_passes_test(lambda u: u.is_admin)
def toggle_cancelar(request, organiza_id):
    organiza = Organiza.objects.get(pk=organiza_id)

    if __contar_pujas(organiza.evento.pk):
        messages.add_message(
            request,
            messages.WARNING,
            "No se puede modificar un evento que tenga transacciones registradas.",
        )
        return redirect("tienda:eventos:list")

    organiza.evento.cancelado = not organiza.evento.cancelado
    organiza.evento.save()

    accion = "cancelado" if organiza.evento.cancelado else "activado"

    messages.add_message(
        request,
        messages.SUCCESS,
        "El evento con ID {} ha sido {}.".format(organiza_id, accion),
    )
    return redirect("tienda:eventos:list")


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_list_tiendas(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    predata = Organiza.objects.filter(pk=organiza_id, tienda_id=tienda_id).get()
    data = Organiza.objects.filter(evento_id=predata.evento_id).all()
    return render(
        request,
        "tienda/eventos/evento_list_tiendas.html",
        {"organiza_id": organiza_id, "data": data},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_add_tienda(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.get(pk=organiza_id)

    in_event = Organiza.objects.filter(evento_id=organiza.evento.pk).all()
    tiendas = (
        Tienda.objects.exclude(pk=tienda_id)
        .exclude(pk__in=in_event.values_list("tienda_id"))
        .all()
    )
    form = OrganizaForm()

    if request.method == "POST":

        if __contar_pujas(organiza.evento.pk):
            messages.add_message(
                request,
                messages.WARNING,
                "No se puede modificar un evento que tenga transacciones registradas.",
            )
            return redirect("tienda:eventos:list")

        list_tiendas = []

        for tienda_id in request.POST.getlist("tienda_id[]"):
            tienda = Tienda.objects.get(pk=tienda_id)
            new_organiza = Organiza()
            new_organiza.tienda = tienda
            new_organiza.evento = organiza.evento
            new_organiza.modified = timezone.now()
            list_tiendas.append(new_organiza)

        if len(list_tiendas):

            if Organiza.objects.bulk_create(list_tiendas):
                messages.add_message(request, messages.SUCCESS, "Cambios guardados.")
                return redirect("tienda:eventos:list")
            else:
                messages.add_message(
                    request, messages.WARNING, "No se realizaron cambios."
                )
        else:
            messages.add_message(request, messages.WARNING, "No se realizaron cambios.")

    return render(
        request,
        "tienda/eventos/evento_add_tienda.html",
        {"form": form, "tiendas": tiendas},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_remove_tienda(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.filter(pk=organiza_id, tienda_id=tienda_id).get()

    if __contar_pujas(organiza.evento.pk):
        messages.add_message(
            request,
            messages.ERROR,
            "No se puede modificar un evento que tenga transacciones registradas.",
        )
        return redirect("tienda:eventos:list")

    total = Organiza.objects.filter(evento_id=organiza.evento.pk).count()

    if total > 1:
        messages.add_message(request, messages.SUCCESS, "Se ha eliminado del Evento.")
        organiza = Organiza.objects.get(pk=organiza_id, tienda_id=tienda_id)
        organiza.evento.delete()
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "No se puede eliminar del Evento, no hay otros organizadores.",
        )

    return redirect("tienda:eventos:list")


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_list_items(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.filter(pk=organiza_id, tienda_id=tienda_id).get()

    data = ObjetoSubastaEvento.objects.filter(evento_id=organiza.evento.pk).all()

    if request.method == "POST":

        if __contar_pujas(organiza.evento.pk):
            messages.add_message(
                request,
                messages.WARNING,
                "No se puede modificar un evento que tenga transacciones registradas.",
            )
            return redirect("tienda:eventos:list")

        objeto_subasta_eventos = request.POST.getlist("objeto_subasta_evento[]")
        eventos = request.POST.getlist("evento[]")
        porc_min_ganancias = request.POST.getlist("porc_min_ganancia[]")
        precios = request.POST.getlist("precio[]")
        ordenes = request.POST.getlist("orden[]")
        duraciones = request.POST.getlist("duracion_minima[]")
        tipo_pujas = request.POST.getlist("tipo_puja[]")
        error_guardando = False

        for i, item in enumerate(objeto_subasta_eventos):

            objeto_subasta_evento = objeto_subasta_eventos[i]
            rec = ObjetoSubastaEvento.objects.get(pk=objeto_subasta_evento)
            rec.orden = ordenes[i]

            if rec.tienda.pk == tienda_id:
                rec.evento = Evento.objects.get(pk=eventos[i])
                rec.porc_min_ganancia = porc_min_ganancias[i]
                rec.precio = precios[i]
                rec.duracion_minima = duraciones[i]
                rec.tipo_puja = tipo_pujas[i]

            try:
                rec.full_clean()
                rec.save()
            except ValidationError:
                error_guardando = True
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Algunos cambios no se pudieron guardar por existir errores.",
                )

        if not error_guardando:
            messages.add_message(request, messages.SUCCESS, "Cambios guardados")

        return redirect("tienda:eventos:event_list_items", organiza_id)

    return render(
        request,
        "tienda/eventos/evento_list_catalogos.html",
        {"organiza_id": organiza_id, "data": data},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_add_item(request, organiza_id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.get(pk=organiza_id)
    in_catalog = ObjetoSubastaEvento.objects.filter(evento_id=organiza.evento.pk).all()
    moneda_ids = in_catalog.exclude(moneda_id__isnull=True).values_list(
        "moneda_id", flat=True
    )
    pintura_ids = in_catalog.exclude(pintura_id__isnull=True).values_list(
        "pintura", flat=True
    )
    pinturas = (
        Pintura.objects.filter(tienda_id=tienda_id, coleccionista_id__isnull=True)
        .exclude(nur__in=pintura_ids)
        .all()
    )
    monedas = (
        Moneda.objects.filter(tienda_id=tienda_id, coleccionista_id__isnull=True)
        .exclude(nur__in=moneda_ids)
        .all()
    )
    catalogos = chain(pinturas, monedas)

    if request.method == "POST":

        catalogo_monedas = request.POST.getlist("catalogo_moneda[]")
        art_monedas = request.POST.getlist("moneda[]")
        art_pinturas = request.POST.getlist("pintura[]")
        eventos = request.POST.getlist("evento[]")
        porc_min_ganancias = request.POST.getlist("porc_min_ganancia[]")
        precios = request.POST.getlist("precio[]")
        ordenes = request.POST.getlist("orden[]")
        duraciones = request.POST.getlist("duracion_minima[]")
        tipo_pujas = request.POST.getlist("tipo_puja[]")
        error_guardando = False

        for i, item in enumerate(catalogo_monedas):

            rec = ObjetoSubastaEvento()
            rec.moneda = (
                Moneda.objects.filter(pk=art_monedas[i]).first()
                if art_monedas[i]
                else None
            )
            rec.pintura = (
                Pintura.objects.filter(pk=art_pinturas[i]).first()
                if art_pinturas[i]
                else None
            )
            rec.orden = ordenes[i]
            rec.duracion_minima = duraciones[i]
            rec.tipo_puja = tipo_pujas[i]
            rec.evento = Evento.objects.get(pk=eventos[i])
            rec.porc_min_ganancia = porc_min_ganancias[i]
            rec.precio = precios[i]
            rec.tienda_id = tienda_id

            try:
                rec.full_clean()
                rec.save()
            except ValidationError:
                error_guardando = True

        if error_guardando:
            messages.add_message(
                request,
                messages.WARNING,
                "Algunos cambios no se pudieron guardar por existir errores.",
            )
        else:
            messages.add_message(request, messages.SUCCESS, "Cambios guardados")

    return render(
        request,
        "tienda/eventos/evento_add_catalogo.html",
        {"catalogos": catalogos, "evento": organiza.evento},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def event_remove_item(request, organiza_id, id):
    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.filter(pk=organiza_id, tienda_id=tienda_id).get()

    if __contar_pujas(organiza.evento.pk):
        messages.add_message(
            request,
            messages.WARNING,
            "No se puede modificar un evento que tenga transacciones registradas.",
        )
        return redirect("tienda:eventos:list")

    objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(
        pk=id, evento_id=organiza.evento.pk
    )
    objeto_subasta_evento.delete()

    messages.add_message(request, messages.SUCCESS, "Registro {} eliminado.".format(id))
    return redirect("tienda:eventos:event_list_items", organiza_id)


@login_required
@user_passes_test(lambda u: u.is_admin)
def get_all_event_report(request):

    tienda_id = request.user.contacto.tienda.pk
    fecha_minima = request.GET.get("fecha_minima", None)
    fecha_maxima = request.GET.get("fecha_maxima", None)
    cancelado = request.GET.get("cancelado", None)
    tipo = request.GET.get("tipo", None)
    generar = request.GET.get("generar", None)

    if generar:

        url = "http://192.168.1.8:5488/api/report"
        headers = {"Content-Type": "application/json"}
        body = {"template": {"shortid": "j9SYkc1bHY"}, "data": {
                "tienda_id": tienda_id,
                "fecha_minima": fecha_minima,
                "fecha_maxima": fecha_maxima,
                "cancelado": cancelado,
                "tipo": tipo,
            }
        }

        response = requests.post(url, data=json.dumps(body), headers=headers)

        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers["Content-Type"],
        )

        return django_response

    return render(request, "tienda/eventos/report.html")


def get_report(request, organiza_id):

    tienda_id = request.user.contacto.tienda.pk
    organiza = Organiza.objects.filter(pk=organiza_id, tienda_id=tienda_id).get()

    url = "http://192.168.1.8:5488/api/report"
    headers = {"Content-Type": "application/json"}
    body = {"template": {"shortid": "2pHWI31SHa"}, "data": {"tienda_id": tienda_id, "evento_id": organiza.evento.pk}}

    response = requests.post(url, data=json.dumps(body), headers=headers)

    django_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers["Content-Type"],
    )

    return django_response
