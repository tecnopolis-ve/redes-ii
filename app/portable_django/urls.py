from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

import subastas_redes.public as public
import subastas_redes.auth as auth

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', auth.registro),
    path('', include(('subastas_redes.public.urls', 'public'), namespace='public'), name='public'),
    path('staff/', include(('subastas_redes.admin.urls', 'staff'), namespace='staff'), name='staff'),
    path('tienda/', include(('subastas_redes.tienda.urls', 'tienda'), namespace='tienda'), name='tienda'),
    path('usuario/', include(('subastas_redes.usuario.urls', 'usuario'), namespace='usuario'), name='usuario'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
