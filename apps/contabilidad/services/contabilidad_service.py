# apps/contabilidad/services/contabilidad_service.py

from apps.contabilidad.models import Cuenta, Transaccion
from django.utils import timezone

def crear_cuenta(nombre_cuenta, tipo_cuenta):
    """
    Crea y guarda una nueva cuenta contable.
    """
    cuenta = Cuenta(nombre_cuenta=nombre_cuenta, tipo_cuenta=tipo_cuenta)
    cuenta.save()
    return cuenta

def obtener_cuenta_por_id(cuenta_id):
    """
    Retorna la cuenta con el ID especificado, o None si no existe.
    """
    try:
        return Cuenta.objects.get(id=cuenta_id)
    except Cuenta.DoesNotExist:
        return None

def listar_cuentas():
    """
    Retorna todas las cuentas contables.
    """
    return Cuenta.objects.all()

def crear_transaccion(cuenta_id, monto, descripcion=""):
    """
    Crea una nueva transacción asociada a la cuenta especificada.
    """
    cuenta = obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        return None

    transaccion = Transaccion(
        cuenta=cuenta,
        monto=monto,
        descripcion=descripcion,
        fecha_transaccion=timezone.now()
    )
    transaccion.save()
    return transaccion

def obtener_transaccion_por_id(transaccion_id):
    """
    Retorna la transacción con el ID especificado, o None si no existe.
    """
    try:
        return Transaccion.objects.get(id=transaccion_id)
    except Transaccion.DoesNotExist:
        return None

def listar_transacciones():
    """
    Retorna todas las transacciones existentes.
    """
    return Transaccion.objects.all()

def listar_transacciones_por_cuenta(cuenta_id):
    """
    Retorna todas las transacciones asociadas a una cuenta específica.
    """
    return Transaccion.objects.filter(cuenta_id=cuenta_id)
