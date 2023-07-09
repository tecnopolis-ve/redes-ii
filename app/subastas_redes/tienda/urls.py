from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.tienda as tienda
import subastas_redes.auth as auth

urlpatterns = [
    path('', tienda.index, name='index'),
    path('detail/', tienda.detail, name='detail'),
    path('productos/', include(('subastas_redes.tienda.productos.urls', 'productos'), namespace='productos')),
    path('clientes/', include(('subastas_redes.tienda.clientes.urls', 'clientes'), namespace='clientes')),
    path('perfil/', include(('subastas_redes.tienda.perfil.urls', 'perfil'), namespace='perfil')),
]