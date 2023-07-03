from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.public.organizadores.organizadores as organizadores

urlpatterns = [
    path('list/', organizadores.list, name='list'),
    re_path(r'^detalle/(?P<id>\d+)$', organizadores.detail, name='detail'),
]