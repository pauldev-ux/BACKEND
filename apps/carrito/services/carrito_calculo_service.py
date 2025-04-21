# apps/carrito/services/carrito_calculo_service.py
from apps.carrito.models import Carrito

def calcular_total(usuario_id):
    carrito = Carrito.objects.filter(usuario_id=usuario_id)
    total = sum([item.producto.precio * item.cantidad for item in carrito])
    return total

def aplicar_descuento(total, descuento):
    return total - (total * (descuento / 100))
