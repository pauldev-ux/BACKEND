# apps/reportes/admin.py

from django.contrib import admin
from apps.reportes.models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'tipo_reporte', 'fecha_generado', 'usuario')
    search_fields = ('titulo', 'descripcion', 'usuario__username')
