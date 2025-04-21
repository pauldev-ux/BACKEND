# apps/voz/models.py

from django.db import models
from django.utils import timezone

from apps.usuarios.models import User  # Ajusta si tu User está en otro lugar

class VozComando(models.Model):
    """
    Modelo que representa la tabla voz_comandos
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comando_recibido = models.TextField()
    resultado_accion = models.TextField(blank=True, null=True)  # Log de ejecución
    fecha_comando = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'voz_comandos'  # Hace match con tu CREATE TABLE voz_comandos

    def __str__(self):
        return f"Comando: {self.comando_recibido[:50]}... - Usuario: {self.usuario}"
