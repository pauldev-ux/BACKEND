# apps/contabilidad/admin.py

from django.contrib import admin
from apps.contabilidad.models import Cuenta, Transaccion

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cuenta', 'tipo_cuenta', 'created_at')
    search_fields = ('nombre_cuenta', 'tipo_cuenta')

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cuenta', 'monto', 'descripcion', 'fecha_transaccion')
    search_fields = ('cuenta__nombre_cuenta', 'descripcion')
    list_filter = ('cuenta__tipo_cuenta', 'fecha_transaccion')
