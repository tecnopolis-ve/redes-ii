from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.public.public as public

urlpatterns = [
    path('', public.index, name='index'),
    path('procesar/', public.procesar, name='procesar'),
    path('subastas/', include(('subastarte.public.subastas.urls', 'subastas'), namespace='subastas')),
    path('organizadores/', include(('subastarte.public.organizadores.urls', 'organizadores'), namespace='organizadores')),
    path('monedas-pinturas/', include(('subastarte.public.articulos.urls', 'articulos'), namespace='articulos')),
]