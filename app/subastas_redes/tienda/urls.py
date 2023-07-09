from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.tienda as tienda
import subastas_redes.auth as auth

urlpatterns = [
    path('', tienda.index, name='index'),
    path('detail/', tienda.detail, name='detail'),
    path('articulos/', include(('subastas_redes.tienda.articulos.urls', 'articulos'), namespace='articulos')),
    path('clientes/', include(('subastas_redes.tienda.clientes.urls', 'clientes'), namespace='clientes')),
    path('perfil/', include(('subastas_redes.tienda.perfil.urls', 'perfil'), namespace='perfil')),
    path('eventos/', include(('subastas_redes.tienda.eventos.urls', 'eventos'), namespace='eventos')),
    path('artistas/', include(('subastas_redes.tienda.artistas.urls', 'artistas'), namespace='artistas')),
]