from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.public.public as public

urlpatterns = [
    path('', public.index, name='index'),
    path('procesar/', public.procesar, name='procesar'),
    path('subastas/', include(('subastas_redes.public.subastas.urls', 'subastas'), namespace='subastas')),
    path('organizadores/', include(('subastas_redes.public.organizadores.urls', 'organizadores'), namespace='organizadores')),
    path('monedas-pinturas/', include(('subastas_redes.public.articulos.urls', 'articulos'), namespace='articulos')),
]