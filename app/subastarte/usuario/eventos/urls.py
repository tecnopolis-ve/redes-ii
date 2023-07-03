from django.urls import path, re_path
from django.conf.urls import url, include
import subastarte.usuario.eventos.eventos as eventos

urlpatterns = [
    path('', eventos.list, name='index'),
]