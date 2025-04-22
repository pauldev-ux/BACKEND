# apps/ventas/services/checkout_service.py

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.cart.models import Cart
from apps.productos.models import Product
from apps.ventas.models import Venta, VentaDetalle
from apps.reportes.exports.sales_pdf_exporter import export_sales_to_pdf

@transaction.atomic
def checkout_usuario(user_id):
    """
    Procesa el checkout para un usuario:
    1. Obtiene el carrito y sus items.
    2. Crea la Venta con fecha y status inicial.
    3. Crea cada VentaDetalle y actualiza stock.
    4. Actualiza total y marca la venta como COMPLETADA.
    5. Vacía el carrito.
    6. Genera el reporte en PDF.
    """
    # 1. Obtener carrito
    try:
        cart = Cart.objects.get(user_id=user_id)
        items = cart.items.select_related('product').all()
        if not items:
            raise ValueError("El carrito está vacío.")
    except Cart.DoesNotExist:
        raise ValueError("El usuario no tiene carrito.")

    # 2. Crear Venta con fecha actual y estado PENDIENTE
    venta = Venta.objects.create(
        usuario_id=user_id,
        total=0,
        status=Venta.Status.PENDIENTE,
        fecha=timezone.now()
    )

    # 3. Procesar ítems: crear detalles y restar stock
    total = 0
    for item in items:
        producto = item.product
        cantidad = item.quantity
        precio_unitario = float(producto.price)

        VentaDetalle.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio=precio_unitario,
        )

        total += cantidad * precio_unitario

        # Actualización atómica del stock
        Product.objects.filter(pk=producto.id).update(
            stock=F('stock') - cantidad
        )

    # 4. Actualizar total y cambiar estado a COMPLETADA
    venta.total = total
    venta.status = Venta.Status.COMPLETADA
    venta.save()

    # 5. Vaciar carrito
    cart.items.all().delete()

    # 6. Generar reporte PDF
    export_sales_to_pdf([venta], user_id)

    return venta
