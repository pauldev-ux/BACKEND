# apps/productos/services/inventario_service.py

from apps.productos.models import Product

def reduce_stock(product_id, amount):
    product = Product.objects.get(id=product_id)
    if product.stock >= amount:
        product.stock -= amount
        product.save()
        return product
    else:
        raise ValueError("No hay suficiente stock")
