from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

import subastarte.public as public
import subastarte.auth as auth

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', auth.registro),
    path('', include(('subastarte.public.urls', 'public'), namespace='public'), name='public'),
    path('staff/', include(('subastarte.admin.urls', 'staff'), namespace='staff'), name='staff'),
    path('tienda/', include(('subastarte.tienda.urls', 'tienda'), namespace='tienda'), name='tienda'),
    path('usuario/', include(('subastarte.usuario.urls', 'usuario'), namespace='usuario'), name='usuario'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
