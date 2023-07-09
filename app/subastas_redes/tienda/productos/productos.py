from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastas_redes.models import Producto
from subastas_redes.forms.producto import ProductoForm
from django.contrib import messages
from django.core.exceptions import ValidationError


@login_required
@user_passes_test(lambda u: u.is_admin)
def list(request):
    tienda_id = request.user.contacto.tienda.pk
    data = Producto.objects.filter(
        tienda_id=tienda_id, coleccionista_id__isnull=True
    ).all()
    return render(request, "tienda/productos/list.html", {"data": data})


@login_required
@user_passes_test(lambda u: u.is_admin)
def detail(request, id):
    producto = Producto.objects.get(pk=id, coleccionista_id__isnull=True)
    return render(
        request, "tienda/productos/detail.html", {"producto": producto}
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def add(request):
    form = ProductoForm()

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.tienda = request.user.contacto.tienda
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, "Cambios guardados.")
                return redirect("tienda:productos:productos")

        else:
            messages.add_message(
                request, messages.WARNING, "Existen errores en el formulario."
            )

    return render(request, "tienda/productos/form.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_admin)
def edit(request, id):
    producto = Producto.objects.get(pk=id, coleccionista_id__isnull=True)
    form = ProductoForm(instance=producto)

    data = []

    if request.method == "POST":

        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.instance.tienda = request.user.contacto.tienda
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, "Cambios guardados.")
                return redirect("tienda:productos:producto_edit", id)

        else:
            messages.add_message(
                request, messages.WARNING, "Existen errores en el formulario."
            )

    return render(
        request,
        "tienda/productos/form.html",
        {"form": form, "data": data, "producto_id": id},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def delete(request, id):
    producto = Producto.objects.get(pk=id, coleccionista_id__isnull=True)
    producto.delete()
    messages.add_message(request, messages.SUCCESS, "Registro {} eliminado.".format(id))
    return redirect("tienda:productos:productos")
