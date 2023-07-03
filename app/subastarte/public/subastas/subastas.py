from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls.base import translate_url
from subastarte.models import Cliente, Evento, ObjetoSubastaEvento, Organiza, Participante, Coleccionista, Puja
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.utils import timezone
from subastarte.forms.puja import PujaForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test

def list(request):
    data = Evento.objects.filter(cancelado=False).all().order_by('-fecha')
    return render(request, "public/subastas/list.html", {'data': data})

def detail(request, id):

    cliente = None
    objeto_subasta_evento = None
    participante = False
    evento_activo = True
    usuario_id = request.user.pk
    evento = Evento.objects.get(pk=id)
    organizadores = Organiza.objects.filter(evento_id=evento.pk).prefetch_related('tienda').all()
    tiendas_id = organizadores.values_list('tienda_id')

    if usuario_id:
        cliente = Cliente.objects.filter(tienda_id__in=tiendas_id).filter(coleccionista__pk=usuario_id).first()
        if cliente:
            participante = Participante.objects.filter(evento_id=evento.pk, cliente_id=cliente.pk)

    if evento.cancelado or evento.fecha + datetime.timedelta(hours=evento.horas) < timezone.now():
        evento_activo = False

    if not evento.cancelado:
        objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(evento_id=evento.pk).order_by('orden').all()[:5]

    return render(request, "public/subastas/detail.html", {
        'evento': evento, 
        'tiendas': organizadores.select_related('tienda').all(), 
        'objeto_subasta_evento': objeto_subasta_evento,
        'participante': participante,
        'cliente': cliente,
        'evento_activo': evento_activo,
    })

@login_required
@user_passes_test(lambda u:not (u.is_admin or u.is_superuser))
def inscribir(request, id):

    participante = False
    usuario_id = request.user.pk
    evento = Evento.objects.get(pk=id)
    organizadores = Organiza.objects.filter(evento_id=evento.pk).all()
    tiendas_id = organizadores.values_list('tienda_id')
    cliente = Cliente.objects.filter(tienda_id__in=tiendas_id).filter(coleccionista__pk=usuario_id).all()

    if cliente:
        clientes_id = cliente.values_list('num_exp_unico')
        participante = Participante.objects.filter(evento_id=evento.pk, cliente_id__in=clientes_id)
        if participante:
            messages.add_message(request, messages.INFO, 'Ya estás inscrito en este evento.')
            return redirect('public:subastas:detail', evento.pk)

    if evento.cancelado or evento.fecha + datetime.timedelta(hours=evento.horas) < timezone.now():
        messages.add_message(request, messages.WARNING, 'Este evento no está disponible.')
        return redirect('public:subastas:detail', evento.pk)

    if request.method == "POST":

        try:

            for tienda in organizadores:

                try:

                    coleccionista = Coleccionista.objects.get(pk=usuario_id)

                    if evento.tipo == 'VIRTUAL' and tienda.tienda.alcance == 'LOCAL':
                        if coleccionista.vive == tienda.tienda.pais:
                            pass
                        else:
                            raise ValidationError('La tienda <b>{}</b> solo admite clientes de {}, por lo tanto, no podrás realizar transacciones con dicha tienda.'.format(tienda.tienda.nombre, tienda.tienda.pais))

                    if coleccionista.edad >= 21:

                        cliente = Cliente.objects.filter(tienda_id=tienda.tienda.pk, coleccionista_id=usuario_id).first()

                        if not cliente:

                            cliente = Cliente()
                            cliente.tienda = tienda.tienda
                            cliente.coleccionista = coleccionista
                            cliente.save()

                        participante = Participante()
                        participante.cliente = cliente
                        participante.evento = evento
                        participante.pais_envio = coleccionista.vive

                        participante.full_clean()
                        participante.save()

                        messages.add_message(request, messages.SUCCESS, 'Tu inscripción ha sido procesada exitosamente.')

                    else:
                        raise ValidationError('La edad mínima requerida es de 21 años para participar.')

                except ValidationError as e:

                    messages.add_message(request, messages.WARNING, e, extra_tags='safe')

                finally:

                    pass

        except Exception as e:
            print(">>>>", e)
            messages.add_message(request, messages.WARNING, 'Error al procesar tu solicitud de inscripción.')
        finally:

            return redirect('public:subastas:detail', evento.pk)

    return render(request, "public/subastas/inscribir.html", {
        'evento': evento, 
        'tiendas': organizadores, 
        'participante': participante,
        'cliente': cliente,
    })