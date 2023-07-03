from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.admin.admin as admin

urlpatterns = [
    path('', admin.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include(('subastarte.admin.users.urls', 'users'), namespace='users')),
    path('tiendas/', include(('subastarte.admin.tiendas.urls', 'tiendas'), namespace='tiendas')),
    path('divisas/', include(('subastarte.admin.divisas.urls', 'divisas'), namespace='divisas')),
    path('paises/', include(('subastarte.admin.paises.urls', 'paises'), namespace='paises')),
]