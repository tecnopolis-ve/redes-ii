from django.shortcuts import render
from subastarte.models import Evento, Factura, ItemFactura, ObjetoSubastaEvento, Puja, CostoEnvioOtros
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from datetime import timedelta
from django.db.models import Max

def index(request):

    subastas = Evento.objects.filter(cancelado=False, fecha__gte=timezone.now().date()).all().order_by('-fecha')[:3]

    return render(request, "public/public/index.html", {'subastas': subastas})

def __calcular_total_manejo_envio(total_monto, costo_envios_otros):

    total_manejo_envio = 0

    if costo_envios_otros.costo_extra:
        total_manejo_envio += total_monto * costo_envios_otros.costo_extra / 100
    if costo_envios_otros.recargo_envio:
        total_manejo_envio += total_monto * costo_envios_otros.recargo_envio / 100
    if costo_envios_otros.embalaje:
        total_manejo_envio += total_monto * costo_envios_otros.embalaje / 100
    if costo_envios_otros.seguro:
        total_manejo_envio += total_monto * costo_envios_otros.seguro / 100

    return total_manejo_envio

def procesar(request):

    eventos = Evento.objects.filter(fecha__lte=timezone.now() - timedelta(minutes=360)).all()

    for evento in eventos:
        facturas = []
        objeto_subasta_evento = ObjetoSubastaEvento.objects.filter(evento=evento.pk, ganador__isnull=True).all()
        costo_envios_otros = CostoEnvioOtros.objects.filter(evento=evento.pk).first()
        for objeto in objeto_subasta_evento:
            if objeto.tipo_puja == 'SOBRE_CERRADO':
                puja_mas_alta = Puja.objects.filter(objeto_subasta_evento=objeto.pk).aggregate(Max('bid')).get('bid__max')
                puja_mas_alta = Puja.objects.filter(objeto_subasta_evento=objeto.pk, bid=puja_mas_alta).first()
                if puja_mas_alta:
                    factura = next((item for item in facturas if item["cliente"] == puja_mas_alta.participante.cliente), None)
                    total_monto = puja_mas_alta.bid
                    if factura:
                        factura['total_monto'] += total_monto
                        factura['total_manejo_envio'] += __calcular_total_manejo_envio(total_monto, costo_envios_otros)
                        factura['items'].append(puja_mas_alta.objeto_subasta_evento)
                    else:
                        elem_factura = {
                            'cliente': puja_mas_alta.participante.cliente,
                            'coleccionista': puja_mas_alta.participante.cliente.coleccionista,
                            'total_monto': total_monto,
                            'total_manejo_envio': __calcular_total_manejo_envio(total_monto, costo_envios_otros),
                            'items': [puja_mas_alta.objeto_subasta_evento]
                        }
                        facturas.append(elem_factura)
                    if objeto.moneda:
                        objeto.moneda.coleccionista = puja_mas_alta.participante.cliente.coleccionista
                        objeto.moneda.save()
                    elif objeto.pintura:
                        objeto.pintura.coleccionista = puja_mas_alta.participante.cliente.coleccionista
                        objeto.pintura.save()
                    objeto.bid = puja_mas_alta.bid
                    objeto.ganador = puja_mas_alta.participante.cliente.coleccionista
                    objeto.save()
            elif objeto.tipo_puja == 'DINAMICA':
                if objeto.bid > 0:
                    puja_mas_alta = Puja.objects.filter(objeto_subasta_evento=objeto.pk).latest('participante')
                    if puja_mas_alta:
                        factura = next((item for item in facturas if item["cliente"] == puja_mas_alta.participante.cliente), None)
                        total_monto = puja_mas_alta.bid
                        if factura:
                            factura['total_monto'] += total_monto
                            factura['total_manejo_envio'] += __calcular_total_manejo_envio(total_monto, costo_envios_otros)
                            factura['items'].append(puja_mas_alta.objeto_subasta_evento)
                        else:
                            elem_factura = {
                                'cliente': puja_mas_alta.participante.cliente,
                                'coleccionista': puja_mas_alta.participante.cliente.coleccionista,
                                'total_monto': total_monto,
                                'total_manejo_envio': __calcular_total_manejo_envio(total_monto, costo_envios_otros),
                                'items': [puja_mas_alta.objeto_subasta_evento]
                            }
                            facturas.append(elem_factura)
                        if objeto.moneda:
                            objeto.moneda.coleccionista = puja_mas_alta.participante.cliente.coleccionista
                            objeto.moneda.save()
                        elif objeto.pintura:
                            objeto.pintura.coleccionista = puja_mas_alta.participante.cliente.coleccionista
                            objeto.pintura.save()
                        objeto.ganador = puja_mas_alta.participante.cliente.coleccionista
                        objeto.save()

        #Genero las facturas por evento
        for factura in facturas:

            new_factura = Factura()
            new_factura.total_monto = factura['total_monto']
            new_factura.total_manejo_envio = factura['total_manejo_envio']
            new_factura.cliente = factura['cliente']
            new_factura.coleccionista = factura['coleccionista']
            new_factura.fecha = timezone.now().date()
            new_factura.save()
            for item in factura['items']:
                new_item_factura = ItemFactura(factura=new_factura)
                new_item_factura.objeto_subasta_evento = item
                new_item_factura.save()


    messages.add_message(request, messages.SUCCESS, 'Procesado')
    return redirect('/')