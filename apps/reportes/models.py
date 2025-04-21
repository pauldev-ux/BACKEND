# apps/reportes/models.py

from django.db import models
from django.utils import timezone
from apps.usuarios.models import User  # Ajusta si tu User está en otro lugar

class Reporte(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo_reporte = models.CharField(max_length=50)  # Ej: 'PDF', 'Excel'
    fecha_generado = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reportes'  # Para que use la tabla "reportes"
    
    def __str__(self):
        return self.titulo
