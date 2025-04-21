# apps/ventas/services/ventas_service.py

from apps.ventas.models import Venta, VentaDetalle
from apps.usuarios.models import User

def crear_venta(usuario_id, total, detalles):
    """
    Crea una nueva venta con sus detalles.
    """
    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        raise ValueError(f"No existe el usuario con ID: {usuario_id}")

    venta = Venta.objects.create(usuario=usuario, total=total)

    for detalle in detalles:
        VentaDetalle.objects.create(
            venta=venta,
            producto_id=detalle['producto_id'],
            cantidad=detalle['cantidad'],
            precio_unitario=detalle['precio']
        )

    return venta

def obtener_ventas_por_usuario(usuario_id):
    """
    Obtiene todas las ventas realizadas por un usuario específico.
    """
    try:
        usuario = User.objects.get(id=usuario_id)
        return Venta.objects.filter(usuario=usuario)
    except User.DoesNotExist:
        return Venta.objects.none()

def actualizar_estado_venta(venta_id, nuevo_estado):
    """
    Actualiza el estado de una venta.
    """
    try:
        venta = Venta.objects.get(id=venta_id)
        venta.status = nuevo_estado
        venta.save()
        return venta
    except Venta.DoesNotExist:
        return None

def procesar_pago(venta_id, metodo_pago, detalles_pago=None):
    """
    Procesa el pago de una venta.
    """
    try:
        venta = Venta.objects.get(id=venta_id)
        venta.status = 'pagado'
        venta.save()
        return True
    except Venta.DoesNotExist:
        return False

def aplicar_descuento(venta_id, porcentaje_descuento):
    """
    Aplica un descuento a una venta.
    """
    try:
        venta = Venta.objects.get(id=venta_id)
        descuento = venta.total * porcentaje_descuento
        venta.total -= descuento
        venta.save()
        return venta
    except Venta.DoesNotExist:
        return None

def generar_recibo_venta(venta_id):
    """
    Genera un recibo de venta para una venta específica.
    """
    try:
        venta = Venta.objects.get(id=venta_id)
        detalles = VentaDetalle.objects.filter(venta=venta)
        recibo = [
            f"--- RECIBO DE VENTA #{venta.id} ---",
            f"Fecha: {venta.created_at}",
            f"Cliente: {venta.usuario.username}",
            "--- Detalles ---",
        ]
        for d in detalles:
            subtotal = d.cantidad * d.precio_unitario
            recibo.append(
                f"Producto ID: {d.producto_id}, Cantidad: {d.cantidad}, "
                f"Precio Unitario: {d.precio_unitario}, Subtotal: {subtotal}"
            )
        recibo.append("-------------------")
        recibo.append(f"Total: {venta.total}")
        return "\n".join(recibo)
    except Venta.DoesNotExist:
        return "Venta no encontrada."
