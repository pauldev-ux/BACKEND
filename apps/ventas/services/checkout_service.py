from django.db import transaction
from apps.cart.models import CartItem
from apps.ventas.services.ventas_service import crear_venta

@transaction.atomic
def checkout_usuario(usuario_id):
    """
    Toma todas las líneas del carrito del usuario,
    crea la Venta con sus detalles y borra el carrito.
    """
    items = CartItem.objects.filter(cart__user_id=usuario_id)
    if not items.exists():
        raise ValueError("El carrito está vacío.")

    detalles = []
    total = 0
    for item in items:
        precio_unitario = float(item.product.price)
        detalles.append({
            'producto_id': item.product.id,
            'cantidad':    item.quantity,
            'precio':      precio_unitario,
        })
        total += item.quantity * precio_unitario

    # crea Venta y VentaDetalle
    venta = crear_venta(usuario_id, total, detalles)

    # vacía carrito
    items.delete()

    return venta
