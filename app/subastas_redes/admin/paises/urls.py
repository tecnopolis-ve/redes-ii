from django.urls import path, re_path
import subastas_redes.admin.paises.paises as paises

urlpatterns = [
    path('', paises.list, name='list'),
    re_path(r'^(?P<id>\d+)$', paises.detail, name='detail'),
    re_path(r'^nuevo$', paises.add, name='new'),
    re_path(r'^editar/(?P<id>\d+)$', paises.edit, name='edit'),
    re_path(r'^borrar/(?P<id>\d+)$', paises.delete, name='delete'),
]