# apps/contabilidad/urls.py

from django.urls import path
from apps.contabilidad.views import (
    CuentaListView,
    CuentaDetailView,
    TransaccionListView,
    TransaccionDetailView
)

urlpatterns = [
    # Cuentas
    path('cuentas/', CuentaListView.as_view(), name='cuentas_list'),
    path('cuentas/<int:cuenta_id>/', CuentaDetailView.as_view(), name='cuentas_detail'),

    # Transacciones
    path('transacciones/', TransaccionListView.as_view(), name='transacciones_list'),
    path('transacciones/<int:transaccion_id>/', TransaccionDetailView.as_view(), name='transacciones_detail'),
]
