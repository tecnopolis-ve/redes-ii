from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.tienda.tienda as tienda
import subastarte.auth as auth

urlpatterns = [
    path('', tienda.index, name='index'),
    path('detail/', tienda.detail, name='detail'),
    path('articulos/', include(('subastarte.tienda.articulos.urls', 'articulos'), namespace='articulos')),
    path('clientes/', include(('subastarte.tienda.clientes.urls', 'clientes'), namespace='clientes')),
    path('perfil/', include(('subastarte.tienda.perfil.urls', 'perfil'), namespace='perfil')),
    path('eventos/', include(('subastarte.tienda.eventos.urls', 'eventos'), namespace='eventos')),
    path('artistas/', include(('subastarte.tienda.artistas.urls', 'artistas'), namespace='artistas')),
]