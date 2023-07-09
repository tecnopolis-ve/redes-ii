from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.usuario.facturas.facturas as facturas

urlpatterns = [
    path('', facturas.list, name='index'),
    re_path(r'^detail/(?P<factura_id>\d+)$', facturas.detail, name='detail'),
]