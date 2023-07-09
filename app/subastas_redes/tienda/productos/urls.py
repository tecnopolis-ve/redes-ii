from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.productos.productos as productos

urlpatterns = [
    re_path(r'^productos/$', productos.list, name='productos'),
    re_path(r'^producto/(?P<id>\d+)$', productos.detail, name='producto_detail'),
    re_path(r'^producto/nuevo$', productos.add, name='producto_new'),
    re_path(r'^producto/editar/(?P<id>\d+)$', productos.edit, name='producto_edit'),
    re_path(r'^producto/borrar/(?P<id>\d+)$', productos.delete, name='producto_delete'),
]