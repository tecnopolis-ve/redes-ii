from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.usuario.usuario as usuario

urlpatterns = [
    path('', usuario.index, name='index'),
    path('detail/', usuario.detail, name='detail'),
    path('eventos/', include(('subastas_redes.usuario.eventos.urls', 'eventos'), namespace='eventos')),
    path('articulos/', include(('subastas_redes.usuario.articulos.urls', 'articulos'), namespace='articulos')),
    path('facturas/', include(('subastas_redes.usuario.facturas.urls', 'facturas'), namespace='facturas')),
]