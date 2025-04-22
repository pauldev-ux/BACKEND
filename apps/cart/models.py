# apps/cart/models.py

from django.db import models
from django.conf import settings
from apps.productos.models import Product

class Cart(models.Model):
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito #{self.pk} de {self.user}"


class CartItem(models.Model):
    cart     = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product  = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        db_table = 'cart_item'
        verbose_name = 'Ítem de Carrito'
        verbose_name_plural = 'Ítems de Carrito'

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"


class Payment(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_payments',
        related_query_name='cart_payment'
    )
    payment_intent_id = models.CharField(max_length=255, unique=True)
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    currency          = models.CharField(max_length=10, default='usd')
    status            = models.CharField(max_length=50)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago {self.payment_intent_id} ({self.status})"
