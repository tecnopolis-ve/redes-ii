from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.usuario.usuario as usuario

urlpatterns = [
    path('', usuario.index, name='index'),
    path('detail/', usuario.detail, name='detail'),
    path('eventos/', include(('subastarte.usuario.eventos.urls', 'eventos'), namespace='eventos')),
    path('articulos/', include(('subastarte.usuario.articulos.urls', 'articulos'), namespace='articulos')),
    path('facturas/', include(('subastarte.usuario.facturas.urls', 'facturas'), namespace='facturas')),
]