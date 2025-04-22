from apps.ventas.models import Venta, VentaDetalle
from apps.usuarios.models import User

def crear_venta(usuario_id, total, detalles):
    """
    Crea una nueva Venta y sus detalles.
    - detalles: lista de dicts con keys 'producto_id','cantidad','precio'
    """
    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        raise ValueError(f"No existe el usuario con ID: {usuario_id}")

    # 1) crea la venta
    venta = Venta.objects.create(usuario=usuario, total=total)

    # 2) crea cada detalle usando el campo 'precio' del modelo
    for d in detalles:
        VentaDetalle.objects.create(
            venta       = venta,
            producto_id = d['producto_id'],
            cantidad    = d['cantidad'],
            precio      = d['precio'],
        )

    return venta

# (el resto de funciones de ventas_service.py permanece igual)
