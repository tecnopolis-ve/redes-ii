from django.urls import path, re_path
from django.conf.urls import url, include
import subastas_redes.tienda.eventos.eventos as eventos

urlpatterns = [
    path('list/', eventos.list, name='list'),
    re_path(r'^(?P<organiza_id>\d+)$', eventos.detail, name='detail'),
    re_path(r'^nuevo', eventos.add, name='new'),
    re_path(r'^editar/(?P<organiza_id>\d+)$', eventos.edit, name='edit'),
    re_path(r'^borrar/(?P<organiza_id>\d+)$', eventos.delete, name='delete'),
    re_path(r'^activar-cancelar/(?P<organiza_id>\d+)$', eventos.toggle_cancelar, name='toggle_cancelar'),
    re_path(r'^event-report/(?P<organiza_id>\d+)$', eventos.get_report, name='get_report'),
    path('all-events-reports/', eventos.get_all_event_report, name='get_all_event_report'),
    # --- Tiendas por evento
    re_path(r'^tiendas/(?P<organiza_id>\d+)$', eventos.event_list_tiendas, name='event_list_tiendas'),
    re_path(r'^tiendas/add/(?P<organiza_id>\d+)$', eventos.event_add_tienda, name='event_add_tienda'),
    re_path(r'^tiendas/remove/(?P<organiza_id>\d+)$', eventos.event_remove_tienda, name='event_remove_tienda'),
    # --- Articulos por evento
    re_path(r'^catalogos/(?P<organiza_id>\d+)$', eventos.event_list_items, name='event_list_items'),
    re_path(r'^catalogos/add/(?P<organiza_id>\d+)$', eventos.event_add_item, name='event_add_item'),
    re_path(r'^catalogos/remove/(?P<organiza_id>\d+)/(?P<id>\d+)$', eventos.event_remove_item, name='event_remove_item'),
]