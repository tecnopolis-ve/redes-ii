from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.usuario.productos.productos as productos

urlpatterns = [
    path('', productos.list, name='index'),
    re_path(r'^detail/(?P<ose_id>\d+)$', productos.detail, name='detail'),
]