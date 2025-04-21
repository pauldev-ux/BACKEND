# apps/contabilidad/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.contabilidad.services.contabilidad_service import (
    crear_cuenta,
    obtener_cuenta_por_id,
    listar_cuentas,
    crear_transaccion,
    obtener_transaccion_por_id,
    listar_transacciones,
    listar_transacciones_por_cuenta
)
from apps.contabilidad.serializers import CuentaSerializer, TransaccionSerializer

class CuentaListView(APIView):
    """
    GET para listar cuentas, POST para crear nueva cuenta.
    """
    permission_classes = [permissions.IsAuthenticated]  # Ajusta según tus necesidades

    def get(self, request):
        cuentas = listar_cuentas()
        serializer = CuentaSerializer(cuentas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre_cuenta = request.data.get('nombre_cuenta')
        tipo_cuenta = request.data.get('tipo_cuenta')

        if not nombre_cuenta or not tipo_cuenta:
            return Response(
                {"detail": "Faltan campos obligatorios (nombre_cuenta, tipo_cuenta)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cuenta = crear_cuenta(nombre_cuenta, tipo_cuenta)
        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CuentaDetailView(APIView):
    """
    GET, PUT, DELETE para una cuenta específica.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request, cuenta_id):
        cuenta = obtener_cuenta_por_id(cuenta_id)
        if not cuenta:
            return Response({"detail": "Cuenta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, cuenta_id):
        cuenta = obtener_cuenta_por_id(cuenta_id)
        if not cuenta:
            return Response({"detail": "Cuenta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        cuenta.nombre_cuenta = request.data.get('nombre_cuenta', cuenta.nombre_cuenta)
        cuenta.tipo_cuenta = request.data.get('tipo_cuenta', cuenta.tipo_cuenta)
        cuenta.save()

        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, cuenta_id):
        cuenta = obtener_cuenta_por_id(cuenta_id)
        if not cuenta:
            return Response({"detail": "Cuenta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        cuenta.delete()
        return Response({"detail": "Cuenta eliminada."}, status=status.HTTP_200_OK)


class TransaccionListView(APIView):
    """
    GET para listar transacciones, POST para crear nueva transacción.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request):
        # Podrías filtrar por cuenta_id si lo recibes como parámetro ?cuenta_id=...
        cuenta_id = request.query_params.get('cuenta_id', None)
        if cuenta_id:
            transacciones = listar_transacciones_por_cuenta(cuenta_id)
        else:
            transacciones = listar_transacciones()

        serializer = TransaccionSerializer(transacciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cuenta_id = request.data.get('cuenta_id')
        monto = request.data.get('monto')
        descripcion = request.data.get('descripcion', '')

        if not cuenta_id or monto is None:
            return Response(
                {"detail": "Faltan campos obligatorios (cuenta_id, monto)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaccion = crear_transaccion(cuenta_id, monto, descripcion)
        if not transaccion:
            return Response({"detail": "No se pudo crear la transacción. Verifica cuenta_id."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TransaccionSerializer(transaccion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransaccionDetailView(APIView):
    """
    GET, PUT, DELETE para una transacción específica.
    """
    "permission_classes = [permissions.IsAuthenticated]"

    def get(self, request, transaccion_id):
        transaccion = obtener_transaccion_por_id(transaccion_id)
        if not transaccion:
            return Response({"detail": "Transacción no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransaccionSerializer(transaccion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, transaccion_id):
        transaccion = obtener_transaccion_por_id(transaccion_id)
        if not transaccion:
            return Response({"detail": "Transacción no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar campos (cuenta_id, monto, descripcion)
        cuenta_id = request.data.get('cuenta_id', None)
        if cuenta_id:
            # Verificamos si existe la nueva cuenta
            nueva_cuenta = obtener_cuenta_por_id(cuenta_id)
            if not nueva_cuenta:
                return Response({"detail": "La cuenta especificada no existe."},
                                status=status.HTTP_400_BAD_REQUEST)
            transaccion.cuenta = nueva_cuenta

        transaccion.monto = request.data.get('monto', transaccion.monto)
        transaccion.descripcion = request.data.get('descripcion', transaccion.descripcion)
        transaccion.save()

        serializer = TransaccionSerializer(transaccion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, transaccion_id):
        transaccion = obtener_transaccion_por_id(transaccion_id)
        if not transaccion:
            return Response({"detail": "Transacción no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        transaccion.delete()
        return Response({"detail": "Transacción eliminada."}, status=status.HTTP_200_OK)
