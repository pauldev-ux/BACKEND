# apps/ventas/services/checkout_service.py

from django.db import transaction
from apps.carrito.models import Carrito
from apps.ventas.services.ventas_service import crear_venta

@transaction.atomic
def checkout_usuario(usuario_id):
    items = Carrito.objects.filter(usuario_id=usuario_id)
    if not items.exists():
        raise ValueError("El carrito está vacío.")

    detalles = []
    total = 0
    for item in items:
        precio = float(item.producto.price)
        detalles.append({
            'producto_id': item.producto_id,
            'cantidad': item.cantidad,
            'precio': precio,
        })
        total += item.cantidad * precio

    venta = crear_venta(usuario_id, total, detalles)
    items.delete()
    return venta
