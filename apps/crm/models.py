# apps/crm/models.py

from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    """
    Asumiendo que ya existe o deseas un modelo para la tabla `crm_clientes`.
    """
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    # Agrega otros campos que necesites...

    class Meta:
        db_table = 'crm_clientes'  # Usa la tabla 'crm_clientes' si así está definida

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    """
    Modelo que mapea la tabla `crm_actividad`.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    fecha_actividad = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'crm_actividad'  # Para que coincida con tu CREATE TABLE

    def __str__(self):
        return f"Actividad de {self.cliente.nombre} - {self.fecha_actividad.strftime('%Y-%m-%d %H:%M:%S')}"
