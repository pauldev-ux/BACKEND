# apps/crm/urls.py

from django.urls import path
from apps.crm.views import (
    ClienteListView,
    ClienteDetailView,
    ActividadListView,
    ActividadDetailView
)

urlpatterns = [
    # Rutas para clientes
    path('clientes/', ClienteListView.as_view(), name='clientes_list'),
    path('clientes/<int:cliente_id>/', ClienteDetailView.as_view(), name='clientes_detail'),

    # Rutas para actividades
    path('actividades/', ActividadListView.as_view(), name='actividades_list'),
    path('actividades/<int:actividad_id>/', ActividadDetailView.as_view(), name='actividades_detail'),
]
