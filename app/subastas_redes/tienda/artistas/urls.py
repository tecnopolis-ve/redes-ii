from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.artistas.artistas as artistas

urlpatterns = [
    path('list/', artistas.list, name='list'),
    re_path(r'^(?P<id>\d+)$', artistas.detail, name='detail'),
    re_path(r'^nuevo', artistas.add, name='new'),
    re_path(r'^editar/(?P<id>\d+)$', artistas.edit, name='edit'),
    re_path(r'^borrar/(?P<id>\d+)$', artistas.delete, name='delete'),
]