from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.public.public as public

urlpatterns = [
    path('', public.index, name='index'),
    path('procesar/', public.procesar, name='procesar'),
    path('productos/', include(('subastas_redes.public.productos.urls', 'productos'), namespace='productos')),
]