from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.productos.productos as productos

urlpatterns = [
    path("list/", productos.list, name="list"),
    re_path(r"^producto/(?P<id>\d+)$", productos.detail, name="detail"),
    re_path(r"^producto/nuevo$", productos.add, name="new"),
    re_path(r"^producto/editar/(?P<id>\d+)$", productos.edit, name="edit"),
    re_path(r"^producto/borrar/(?P<id>\d+)$", productos.delete, name="delete"),
]
