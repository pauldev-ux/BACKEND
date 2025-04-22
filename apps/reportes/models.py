
from django.db import models
from django.utils import timezone
from apps.usuarios.models import User

class Reporte(models.Model):
    titulo        = models.CharField(max_length=255)
    descripcion   = models.TextField(blank=True, null=True)
    tipo_reporte  = models.CharField(max_length=50)  # 'PDF' o 'EXCEL'
    fecha_generado= models.DateTimeField(default=timezone.now)
    usuario       = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo       = models.FileField(upload_to='reportes/', null=True, blank=True)

    class Meta:
        db_table = 'reportes'

    def __str__(self):
        return self.titulo
