from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from subastarte.models import ArtistaPintura, Pintura, Artista
from subastarte.forms.pintura import PinturaForm
from django.contrib import messages
from django.core.exceptions import ValidationError

@login_required
@user_passes_test(lambda u:u.is_admin)
def list(request):
    tienda_id = request.user.contacto.tienda.pk
    data = Pintura.objects.filter(tienda_id=tienda_id, coleccionista_id__isnull=True).all()
    return render(request, "tienda/pinturas/list.html", {'data': data})

@login_required
@user_passes_test(lambda u:u.is_admin)
def detail(request, id):
    pintura = Pintura.objects.get(pk=id, coleccionista_id__isnull=True)
    artistas = ArtistaPintura.objects.filter(pintura=pintura.pk).all()
    return render(request, "tienda/pinturas/detail.html", {'pintura': pintura, 'artistas': artistas})

@login_required
@user_passes_test(lambda u:u.is_admin)
def add(request):
    form = PinturaForm()

    if request.method == "POST":
        form = PinturaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.tienda = request.user.contacto.tienda
            data = form.save()

            if data is not None:
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                return redirect('tienda:articulos:pinturas')

        else:
            messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/pinturas/form.html", {'form': form})

@login_required
@user_passes_test(lambda u:u.is_admin)
def edit(request, id):
    pintura = Pintura.objects.get(pk=id, coleccionista_id__isnull=True)
    artista_pintura = ArtistaPintura.objects.filter(pintura_id=pintura.pk).all()
    artistas = Artista.objects.all().values()
    form = PinturaForm(instance=pintura)

    data = []

    for artista in artistas:

        artist_item = artista

        for item in artista_pintura:
            if (item.artista.pk == artista['id']):
                artist_item['presente'] = True

        data.append(artist_item)

    if request.method == "POST":
        
        if (request.POST.get('artists')):

            ArtistaPintura.objects.filter(pintura_id=pintura.pk).delete()
            artistas = request.POST.getlist('artista_id[]')
            error_guardando = False

            for i,item in enumerate(artistas):

                rec = ArtistaPintura()
                rec.pintura = pintura
                rec.artista = Artista.objects.get(pk=artistas[i])

                try:
                    rec.full_clean()
                    rec.save()
                except ValidationError:
                    error_guardando = True
                    messages.add_message(request, messages.WARNING, 'Algunos cambios no se pudieron guardar por existir errores.')

            if not error_guardando:
                messages.add_message(request, messages.SUCCESS, 'Artistas actualizados.')

            return redirect('tienda:articulos:pintura_edit', id)
        else:

            form = PinturaForm(request.POST, request.FILES, instance=pintura)
            if form.is_valid():
                form.instance.tienda = request.user.contacto.tienda
                data = form.save()

                if data is not None:
                    messages.add_message(request, messages.SUCCESS, 'Cambios guardados.')
                    return redirect('tienda:articulos:pintura_edit', id)

            else:
                messages.add_message(request, messages.WARNING, 'Existen errores en el formulario.')

    return render(request, "tienda/pinturas/form.html", {'form': form, 'data': data, 'pintura_id': id})

@login_required
@user_passes_test(lambda u:u.is_admin)
def delete(request, id):
    pintura = Pintura.objects.get(pk=id, coleccionista_id__isnull=True)
    pintura.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro {} eliminado.'.format(id))
    return redirect('tienda:articulos:pinturas')