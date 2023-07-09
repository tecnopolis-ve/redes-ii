from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.public.subastas.subastas as subastas

urlpatterns = [
    path('list/', subastas.list, name='list'),
    re_path(r'^detalle/(?P<id>\d+)$', subastas.detail, name='detail'),
    re_path(r'^inscribir/(?P<id>\d+)$', subastas.inscribir, name='inscribir'),
]