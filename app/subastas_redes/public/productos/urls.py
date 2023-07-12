from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.public.productos.productos as articulo

urlpatterns = [
    path('list/', articulo.list, name='list'),
    re_path(r'^list/tiendas/(?P<tienda_id>\d+)/', articulo.list, name='list_tienda'),
    re_path(r'^list/subastas/(?P<subasta_id>\d+)/', articulo.list, name='list_subasta'),
    re_path(r'^(?P<articulo_id>\d+)$', articulo.detail, name='detail'),
]