# apps/voz/admin.py

from django.contrib import admin
from apps.voz.models import VozComando

@admin.register(VozComando)
class VozComandoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'comando_recibido', 'resultado_accion', 'fecha_comando')
    search_fields = ('usuario__username', 'comando_recibido', 'resultado_accion')
    list_filter = ('fecha_comando',)
