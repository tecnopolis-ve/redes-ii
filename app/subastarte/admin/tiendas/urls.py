from django.urls import path, re_path
import subastarte.admin.tiendas.tiendas as tiendas
import subastarte.admin.tiendas.contactos as contactos

urlpatterns = [
    path('', tiendas.list, name='list'),
    re_path(r'^(?P<id>\d+)$', tiendas.detail, name='detail'),
    re_path(r'^nuevo$', tiendas.add, name='new'),
    re_path(r'^editar/(?P<id>\d+)$', tiendas.edit, name='edit'),
    re_path(r'^borrar/(?P<id>\d+)$', tiendas.delete, name='delete'),
    # --- CONTACTOS
    re_path(r'^(?P<id>\d+)/contactos/$', contactos.list, name='contactos'),
    re_path(r'^contactos/details/(?P<id>\d+)$', contactos.detail, name='contacto_detail'),
    re_path(r'^(?P<tienda_id>\d+)/contactos/nuevo/$', contactos.add, name='contacto_new'),
    re_path(r'^contactos/editar/(?P<id>\d+)$', contactos.edit, name='contacto_edit'),
    re_path(r'^contactos/borrar/(?P<id>\d+)$', contactos.delete, name='contacto_delete'),
]