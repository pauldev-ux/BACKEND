# apps/voz/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.voz.services.voz_service import (
    crear_comando,
    obtener_comando_por_id,
    listar_comandos,
    listar_comandos_por_usuario
)
from apps.voz.serializers import VozComandoSerializer

class VozComandoListView(APIView):
    """
    GET para listar comandos (opcionalmente filtrar por usuario_id),
    POST para crear un nuevo comando.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request):
        usuario_id = request.query_params.get('usuario_id', None)
        if usuario_id:
            comandos = listar_comandos_por_usuario(usuario_id)
        else:
            comandos = listar_comandos()

        serializer = VozComandoSerializer(comandos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        usuario_id = request.data.get('usuario_id')
        comando_recibido = request.data.get('comando_recibido')
        resultado_accion = request.data.get('resultado_accion', '')

        if not comando_recibido:
            return Response(
                {"detail": "Falta el campo 'comando_recibido'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        comando = crear_comando(usuario_id, comando_recibido, resultado_accion)
        serializer = VozComandoSerializer(comando)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VozComandoDetailView(APIView):
    """
    GET, PUT, DELETE para un comando de voz específico.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request, comando_id):
        comando = obtener_comando_por_id(comando_id)
        if not comando:
            return Response(
                {"detail": "Comando no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = VozComandoSerializer(comando)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comando_id):
        comando = obtener_comando_por_id(comando_id)
        if not comando:
            return Response({"detail": "Comando no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar campos
        usuario_id = request.data.get('usuario_id', None)
        if usuario_id:
            from apps.usuarios.models import User
            try:
                user = User.objects.get(id=usuario_id)
                comando.usuario = user
            except User.DoesNotExist:
                pass  # O podrías retornar error si es obligatorio

        comando_recibido = request.data.get('comando_recibido', None)
        if comando_recibido is not None:
            comando.comando_recibido = comando_recibido

        comando.resultado_accion = request.data.get('resultado_accion', comando.resultado_accion)
        comando.save()

        serializer = VozComandoSerializer(comando)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, comando_id):
        comando = obtener_comando_por_id(comando_id)
        if not comando:
            return Response({"detail": "Comando no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        comando.delete()
        return Response({"detail": "Comando eliminado."}, status=status.HTTP_200_OK)
