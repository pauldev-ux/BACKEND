# apps/reportes/services/reporte_service.py

from django.utils import timezone
from apps.reportes.models import Reporte
from apps.usuarios.models import User  # Ajusta si tu User está en otro lugar

def create_reporte(titulo, descripcion, tipo_reporte, user_id):
    """
    Crea un nuevo reporte en la base de datos.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

    nuevo_reporte = Reporte(
        titulo=titulo,
        descripcion=descripcion,
        tipo_reporte=tipo_reporte,
        fecha_generado=timezone.now(),
        usuario=user
    )
    nuevo_reporte.save()

    return nuevo_reporte

def get_reporte_by_id(reporte_id):
    """
    Retorna un reporte dado su ID, o None si no existe.
    """
    try:
        return Reporte.objects.get(id=reporte_id)
    except Reporte.DoesNotExist:
        return None

def list_reportes():
    """
    Retorna todos los reportes disponibles.
    """
    return Reporte.objects.all()
