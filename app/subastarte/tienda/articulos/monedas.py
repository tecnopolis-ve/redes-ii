from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import ArtistaMoneda, Moneda, Artista
from subastarte.forms.moneda import MonedaForm
from django.contrib import messages
from django.core.exceptions import ValidationError

@login_required
@user_passes_test(lambda u:u.is_admin)
def list(request):
    tienda_id = request.user.contacto.tienda.pk
    data = Moneda.objects.filter(tienda_id=tienda_id, coleccionista_id__isnull=True).all()
    return render(request, "tienda/monedas/list.html", {'data': data})

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request, id):
    moneda = Moneda.objects.get(pk=id, coleccionista_id__isnull=True)
    artistas = ArtistaMoneda.objects.filter(moneda=moneda.pk).all()
    return render(request, "tienda/monedas/detail.html", {'moneda': moneda, 'artistas': artistas})

@login_required
@user_passes_test(lambda u:u.is_admin)
def add(request):
    form = MonedaForm()

    if request.method == "POST":
        form = MonedaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.tienda = request.user.contacto.tienda
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:articulos:monedas')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/monedas/form.html", {'form': form})

@login_required
@user_passes_test(lambda u:u.is_admin)
def edit(request, id):
    moneda = Moneda.objects.get(pk=id, coleccionista_id__isnull=True)
    artista_moneda = ArtistaMoneda.objects.filter(moneda_id=moneda.pk).all()
    artistas = Artista.objects.all().values()
    form = MonedaForm(instance=moneda)

    data = []

    for artista in artistas:

        artist_item = artista

        for item in artista_moneda:
            if (item.artista.pk == artista['id']):
                artist_item['presente'] = True

        data.append(artist_item)

    if request.method == "POST":

        if (request.POST.get('artists')):

            ArtistaMoneda.objects.filter(moneda_id=moneda.pk).delete()
            artistas = request.POST.getlist('artista_id[]')
            error_guardando = False

            for i,item in enumerate(artistas):

                rec = ArtistaMoneda()
                rec.moneda = moneda
                rec.artista = Artista.objects.get(pk=artistas[i])

                try:
                    rec.full_clean()
                    rec.save()
                except ValidationError:
                    error_guardando = True
                    messages.add_message(request, messages.WARNING, 'Algunos cambios no se pudieron guardar por existir errores.')

            if not error_guardando:
                messages.add_message(request, messages.SUCCESS, 'Artistas actualizados.')

            return redirect('tienda:articulos:moneda_edit', id)
        else:

            form = MonedaForm(request.POST, request.FILES, instance=moneda)
            if form.is_valid():
                form.instance.tienda = request.user.contacto.tienda
                data = form.save()

                if data is not None:
                    messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                    return redirect('tienda:articulos:moneda_edit', id)

            else:
                messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/monedas/form.html", {'form': form, 'data': data, 'moneda_id': id})

@login_required
@user_passes_test(lambda u:u.is_admin)
def delete(request, id):
    moneda = Moneda.objects.get(pk=id, coleccionista_id__isnull=True)
    moneda.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('tienda:articulos:monedas')