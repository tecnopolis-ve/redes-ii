from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.usuario.articulos.articulos as articulos

urlpatterns = [
    path('', articulos.list, name='index'),
    re_path(r'^detail/(?P<ose_id>\d+)$', articulos.detail, name='detail'),
]