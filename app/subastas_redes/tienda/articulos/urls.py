from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.articulos.monedas as monedas
import subastas_redes.tienda.articulos.pinturas as pinturas

urlpatterns = [
    # --- MONEDAS
    re_path(r'^monedas/$', monedas.list, name='monedas'),
    re_path(r'^moneda/(?P<id>\d+)$', monedas.detail, name='moneda_detail'),
    re_path(r'^moneda/nuevo$', monedas.add, name='moneda_new'),
    re_path(r'^moneda/editar/(?P<id>\d+)$', monedas.edit, name='moneda_edit'),
    re_path(r'^moneda/borrar/(?P<id>\d+)$', monedas.delete, name='moneda_delete'),
    # --- PINTURAS
    re_path(r'^pinturas/$', pinturas.list, name='pinturas'),
    re_path(r'^pintura/(?P<id>\d+)$', pinturas.detail, name='pintura_detail'),
    re_path(r'^pintura/nuevo', pinturas.add, name='pintura_new'),
    re_path(r'^pintura/editar/(?P<id>\d+)$', pinturas.edit, name='pintura_edit'),
    re_path(r'^pintura/borrar/(?P<id>\d+)$', pinturas.delete, name='pintura_delete'),
]