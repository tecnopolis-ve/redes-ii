from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.tienda.tienda as tienda
import subastarte.tienda.perfil.perfil as perfil

urlpatterns = [
    path('', tienda.index, name='index'),
    path('detail/', perfil.detail, name='detail'),
]