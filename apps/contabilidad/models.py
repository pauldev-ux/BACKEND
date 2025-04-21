# apps/contabilidad/models.py

from django.db import models
from django.utils import timezone

class Cuenta(models.Model):
    """
    Representa una cuenta contable (Activo, Pasivo, Patrimonio, etc.).
    """
    nombre_cuenta = models.CharField(max_length=255)
    tipo_cuenta = models.CharField(max_length=50)  # Ej: 'Activo', 'Pasivo', 'Patrimonio', etc.
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'contabilidad_cuentas'  # Usa la tabla contabilidad_cuentas

    def __str__(self):
        return f"{self.nombre_cuenta} ({self.tipo_cuenta})"

class Transaccion(models.Model):
    """
    Representa una transacción asociada a una cuenta contable.
    """
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    fecha_transaccion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'contabilidad_transacciones'  # Usa la tabla contabilidad_transacciones

    def __str__(self):
        return f"Transacción {self.id} - Cuenta: {self.cuenta.nombre_cuenta} - Monto: {self.monto}"
