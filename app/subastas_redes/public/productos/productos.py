from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from subastas_redes.models import Puja, Cliente, Tienda, Producto
from subastas_redes.forms.puja import PujaForm
from django.db.models import Q
from functools import reduce
from django.utils import timezone
from django.contrib import messages
from itertools import chain
import operator, datetime


def list(request, subasta_id=None, tienda_id=None):

    precio_minimo = request.GET.get("precio_minimo", None)
    precio_maximo = request.GET.get("precio_maximo", None)

    filtros_and = []
    filtros_or = []
    or_cond = None

    if subasta_id:

        if precio_minimo:
            filtros_and.append(Q(ask__gte=precio_minimo))

        if precio_maximo:
            filtros_and.append(Q(ask__lte=precio_maximo))

        if filtros_or:
            or_cond = reduce(operator.or_, filtros_or)
            productos = productos.filter(or_cond)

        if filtros_and:
            and_cond = reduce(operator.and_, filtros_and)
            productos = productos.filter(and_cond)

        paginator = Paginator(productos, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "public/productos/list-subasta.html",
            {
                "data": page_obj,
            },
        )

    elif tienda_id:

        tienda = Tienda.objects.filter(pk=tienda_id).first()

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request, "public/productos/list.html", {"tienda": tienda, "data": page_obj}
        )

    else:
        productos = Producto.objects.filter().all()

        paginator = Paginator(productos, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "public/productos/list.html", {"data": page_obj})


def detail(request, producto_id):

    render_view = None
    item_admite_ofertas = True
    form = None

    usuario_id = request.user.pk
    usuario_ganador = None
    es_ganador = False

    producto = Producto.objects.get(pk=producto_id)

    try:
        usuario_ganador = Puja.objects.get(producto=producto_id, ganador=True)
        es_ganador = usuario_id == usuario_ganador.participante.pk
    except Exception as e:
        pass

    render_view = "public/productos/detail.html"

    if usuario_id:
        puja = Puja()
        puja.participante = request.user
        puja.producto = producto
        form = PujaForm(instance=puja)

    item_admite_ofertas = (producto.fecha_inicio + datetime.timedelta(days=producto.duracion) < timezone.now()) or not usuario_ganador

    if request.method == "POST":
        form = PujaForm(data=request.POST)
        if form.is_valid() and not usuario_ganador:
            producto.bid = form.data.get("bid")
            producto.save()
            data = form.save()

            if data is not None:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Hemos registrado tu oferta correctamente.",
                )

                return redirect("public:productos:detail", producto_id)

        else:
            messages.add_message(
                request,
                messages.WARNING,
                "No hemos podido procesar tu solicitud porque contiene errores.",
            )

    return render(
        request,
        render_view,
        {
            "producto": producto,
            "item_admite_ofertas": item_admite_ofertas,
            "participante": usuario_id,
            "form": form,
            "es_ganador": es_ganador,
            "usuario_ganador": usuario_ganador
        },
    )
