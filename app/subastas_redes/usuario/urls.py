from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.usuario.usuario as usuario

urlpatterns = [
    path('', usuario.index, name='index'),
    path('detail/', usuario.detail, name='detail'),
    path('productos/', include(('subastas_redes.usuario.productos.urls', 'productos'), namespace='productos')),
    path('facturas/', include(('subastas_redes.usuario.facturas.urls', 'facturas'), namespace='facturas')),
]