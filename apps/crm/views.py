# apps/crm/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.crm.services.crm_service import (
    crear_cliente,
    obtener_cliente_por_id,
    listar_clientes,
    crear_actividad,
    obtener_actividad_por_id,
    listar_actividades,
    listar_actividades_por_cliente
)
from apps.crm.serializers import ClienteSerializer, ActividadSerializer

# =========================
#         CLIENTE
# =========================
class ClienteListView(APIView):
    """
    GET para listar clientes, POST para crear un nuevo cliente.
    """
    #permission_classes = [permissions.IsAuthenticated]  # Ajusta según tu lógica

    def get(self, request):
        clientes = listar_clientes()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre')
        email = request.data.get('email')
        telefono = request.data.get('telefono', '')

        if not nombre or not email:
            return Response(
                {"detail": "Faltan campos obligatorios (nombre, email)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cliente = crear_cliente(nombre, email, telefono)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClienteDetailView(APIView):
    """
    GET, PUT, DELETE para un cliente específico.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request, cliente_id):
        cliente = obtener_cliente_por_id(cliente_id)
        if not cliente:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, cliente_id):
        cliente = obtener_cliente_por_id(cliente_id)
        if not cliente:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        cliente.nombre = request.data.get('nombre', cliente.nombre)
        cliente.email = request.data.get('email', cliente.email)
        cliente.telefono = request.data.get('telefono', cliente.telefono)
        cliente.save()

        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, cliente_id):
        cliente = obtener_cliente_por_id(cliente_id)
        if not cliente:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        cliente.delete()
        return Response({"detail": "Cliente eliminado."}, status=status.HTTP_200_OK)

# =========================
#       ACTIVIDAD
# =========================
class ActividadListView(APIView):
    """
    GET para listar actividades (opcionalmente filtrar por cliente_id),
    POST para crear nueva actividad.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request):
        # Si deseas filtrar por ?cliente_id=...
        cliente_id = request.query_params.get('cliente_id', None)
        if cliente_id:
            actividades = listar_actividades_por_cliente(cliente_id)
        else:
            actividades = listar_actividades()

        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cliente_id = request.data.get('cliente_id')
        descripcion = request.data.get('descripcion', '')

        if not cliente_id:
            return Response(
                {"detail": "Falta cliente_id para crear la actividad."},
                status=status.HTTP_400_BAD_REQUEST
            )

        actividad = crear_actividad(cliente_id, descripcion)
        if actividad is None:
            return Response(
                {"detail": "No se pudo crear la actividad. Verifica el cliente_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ActividadSerializer(actividad)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActividadDetailView(APIView):
    """
    GET, PUT, DELETE para una actividad específica.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request, actividad_id):
        actividad = obtener_actividad_por_id(actividad_id)
        if not actividad:
            return Response({"detail": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActividadSerializer(actividad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, actividad_id):
        actividad = obtener_actividad_por_id(actividad_id)
        if not actividad:
            return Response({"detail": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Posibilidad de cambiar el cliente de la actividad
        nuevo_cliente_id = request.data.get('cliente_id', None)
        if nuevo_cliente_id:
            from apps.crm.services.crm_service import obtener_cliente_por_id
            nuevo_cliente = obtener_cliente_por_id(nuevo_cliente_id)
            if not nuevo_cliente:
                return Response(
                    {"detail": "El cliente especificado no existe."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            actividad.cliente = nuevo_cliente

        actividad.descripcion = request.data.get('descripcion', actividad.descripcion)
        actividad.save()

        serializer = ActividadSerializer(actividad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, actividad_id):
        actividad = obtener_actividad_por_id(actividad_id)
        if not actividad:
            return Response({"detail": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        actividad.delete()
        return Response({"detail": "Actividad eliminada."}, status=status.HTTP_200_OK)
