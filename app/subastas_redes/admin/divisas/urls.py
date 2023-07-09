from django.urls import path, re_path
import subastas_redes.admin.divisas.divisas as divisas

urlpatterns = [
    path('', divisas.list, name='list'),
    re_path(r'^(?P<id>\d+)$', divisas.detail, name='detail'),
    re_path(r'^nuevo$', divisas.add, name='new'),
    re_path(r'^editar/(?P<id>\d+)$', divisas.edit, name='edit'),
    re_path(r'^borrar/(?P<id>\d+)$', divisas.delete, name='delete'),
]