# apps/ventas/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from apps.productos.models import Product  # Importa tu modelo real

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Venta(TimestampedModel):
    class Status(models.TextChoices):
        PENDIENTE   = 'pendiente',   _('Pendiente')
        COMPLETADA  = 'completada',  _('Completada')
        CANCELADA   = 'cancelada',   _('Cancelada')

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Importe total de la venta')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDIENTE,
        db_index=True
    )

    class Meta:
        db_table = 'ventas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.get_status_display()} #{self.id} – {self.usuario.username}"

    def update_total(self):
        # Recalcula total sumando cantidad × precio de cada detalle
        total = sum(det.cantidad * det.precio for det in self.detalles.all())
        self.total = total
        self.save(update_fields=['total'])


class VentaDetalle(TimestampedModel):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='ventas_detalle'
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text=_('Cantidad de unidades vendidas')
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Precio unitario al momento de la venta')
    )

    class Meta:
        db_table = 'venta_detalle'

    def __str__(self):
        return f"{self.producto} × {self.cantidad} (Venta #{self.venta.id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Después de guardar un detalle, actualiza el total de la venta padre
        self.venta.update_total()
