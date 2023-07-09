from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.tienda as tienda
import subastas_redes.tienda.perfil.perfil as perfil

urlpatterns = [
    path('', tienda.index, name='index'),
    path('detail/', perfil.detail, name='detail'),
]