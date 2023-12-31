from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.public.productos.productos as producto

urlpatterns = [
    path('list/', producto.list, name='list'),
    re_path(r'^list/tiendas/(?P<tienda_id>\d+)/', producto.list, name='list_tienda'),
    re_path(r'^list/subastas/(?P<subasta_id>\d+)/', producto.list, name='list_subasta'),
    re_path(r'^(?P<producto_id>\d+)$', producto.detail, name='detail'),
]