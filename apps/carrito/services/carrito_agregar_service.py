from apps.carrito.models import Carrito
from apps.productos.models import Product
from django.core.exceptions import ValidationError

def agregar_producto_al_carrito(usuario_id, producto_id, cantidad):
    if cantidad <= 0:
        raise ValidationError("La cantidad debe ser mayor a cero.")

    try:
        producto = Product.objects.get(id=producto_id)
    except Product.DoesNotExist:
        raise ValidationError("Producto no encontrado.")

    if producto.stock < cantidad:
        raise ValidationError(f"No hay suficiente stock. Stock disponible: {producto.stock}")

    carrito_item, creado = Carrito.objects.get_or_create(
        usuario_id=usuario_id,
        producto_id=producto_id,
        defaults={"cantidad": cantidad}
    )

    if not creado:
        nueva_cantidad = carrito_item.cantidad + cantidad
        if producto.stock < nueva_cantidad:
            raise ValidationError(f"No hay suficiente stock para agregar {cantidad} más. Stock actual: {producto.stock}")
        carrito_item.cantidad = nueva_cantidad
        carrito_item.save()

    return carrito_item
