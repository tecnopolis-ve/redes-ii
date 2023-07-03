from django.urls import path, re_path
import subastarte.admin.users.users as users

urlpatterns = [
    path('', users.list, name='list'),
    re_path(r'^(?P<id>\d+)$', users.detail, name='detail'),
    re_path(r'^nuevo$', users.add, name='new'),
    re_path(r'^editar/(?P<id>\d+)$', users.edit, name='edit'),
    re_path(r'^borrar/(?P<id>\d+)$', users.delete, name='delete'),
]