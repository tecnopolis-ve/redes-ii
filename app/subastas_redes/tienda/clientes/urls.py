from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.clientes.clientes as clientes

urlpatterns = [
    path('list/', clientes.list, name='list'),
    re_path(r'^detail/(?P<id>\d+)$', clientes.detail, name='detail'),
]