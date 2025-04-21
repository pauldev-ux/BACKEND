# apps/crm/services/crm_service.py

from django.utils import timezone
from apps.crm.models import Cliente, Actividad

# =========================
#      CLIENTES
# =========================
def crear_cliente(nombre, email, telefono=""):
    """
    Crea un nuevo cliente en la base de datos.
    """
    cliente = Cliente(nombre=nombre, email=email, telefono=telefono)
    cliente.save()
    return cliente

def obtener_cliente_por_id(cliente_id):
    """
    Retorna el cliente con el ID especificado, o None si no existe.
    """
    try:
        return Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return None

def listar_clientes():
    """
    Retorna todos los clientes.
    """
    return Cliente.objects.all()

# =========================
#      ACTIVIDADES
# =========================
def crear_actividad(cliente_id, descripcion=""):
    """
    Crea una nueva actividad asociada a un cliente.
    """
    cliente = obtener_cliente_por_id(cliente_id)
    if not cliente:
        return None
    
    actividad = Actividad(
        cliente=cliente,
        descripcion=descripcion,
        fecha_actividad=timezone.now()
    )
    actividad.save()
    return actividad

def obtener_actividad_por_id(actividad_id):
    """
    Retorna la actividad con el ID especificado, o None si no existe.
    """
    try:
        return Actividad.objects.get(id=actividad_id)
    except Actividad.DoesNotExist:
        return None

def listar_actividades():
    """
    Retorna todas las actividades.
    """
    return Actividad.objects.all()

def listar_actividades_por_cliente(cliente_id):
    """
    Retorna todas las actividades para un cliente específico.
    """
    return Actividad.objects.filter(cliente_id=cliente_id)
