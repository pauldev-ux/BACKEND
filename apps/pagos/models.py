# apps/pagos/models.py

from django.db import models
from django.conf import settings

class Payment(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pagos_payments',
        related_query_name='pagos_payment'
    )
    payment_intent_id = models.CharField(max_length=255, unique=True)
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    currency          = models.CharField(max_length=10, default='usd')
    status            = models.CharField(max_length=50)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Si quieres un nombre de tabla explícito, descomenta:
        # db_table = 'pagos_payment'
        verbose_name = 'Pago (módulo pagos)'
        verbose_name_plural = 'Pagos (módulo pagos)'

    def __str__(self):
        return f"Pago {self.payment_intent_id} ({self.status})"
