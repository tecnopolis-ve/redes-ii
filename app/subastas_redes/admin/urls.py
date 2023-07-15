from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.admin.admin as admin

urlpatterns = [
    path('', admin.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include(('subastas_redes.admin.users.urls', 'users'), namespace='users')),
    path('tiendas/', include(('subastas_redes.admin.tiendas.urls', 'tiendas'), namespace='tiendas')),
]