# apps/voz/services/voz_service.py

from django.utils import timezone
from apps.voz.models import VozComando
from apps.usuarios.models import User  # Ajusta si tu User está en otro lugar

def crear_comando(usuario_id, comando_recibido, resultado_accion=""):
    """
    Crea un registro de comando de voz en la base de datos.
    """
    try:
        user = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        user = None  # O podrías retornar None si es obligatorio que exista el usuario

    comando = VozComando(
        usuario=user,
        comando_recibido=comando_recibido,
        resultado_accion=resultado_accion,
        fecha_comando=timezone.now()
    )
    comando.save()
    return comando

def obtener_comando_por_id(comando_id):
    """
    Retorna un comando de voz por su ID, o None si no existe.
    """
    try:
        return VozComando.objects.get(id=comando_id)
    except VozComando.DoesNotExist:
        return None

def listar_comandos():
    """
    Retorna todos los comandos de voz registrados.
    """
    return VozComando.objects.all()

def listar_comandos_por_usuario(usuario_id):
    """
    Retorna todos los comandos de un usuario específico.
    """
    return VozComando.objects.filter(usuario_id=usuario_id)
