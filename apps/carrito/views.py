# apps/carrito/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError

from apps.carrito.models import Carrito
from apps.carrito.serializers import CarritoSerializer
from apps.carrito.services.carrito_calculo_service import calcular_total, aplicar_descuento
from apps.carrito.services.carrito_pago_service import realizar_pago
from apps.carrito.services.carrito_recibo_service import generar_recibo
from apps.carrito.services.carrito_agregar_service import agregar_producto_al_carrito


class CarritoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, usuario_id):
        # Sólo el propio usuario puede consultar su carrito
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        items      = Carrito.objects.filter(usuario_id=usuario_id)
        serializer = CarritoSerializer(items, many=True)

        total           = calcular_total(usuario_id)
        descuento_param = request.query_params.get('descuento', '0')
        try:
            descuento_pct = float(descuento_param)
        except ValueError:
            return Response({'detail': 'Descuento inválido'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'items': serializer.data,
            'total': total,
            'total_con_descuento': aplicar_descuento(total, descuento_pct)
        }, status=status.HTTP_200_OK)

    def post(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        producto_id = request.data.get('producto_id')
        cantidad     = request.data.get('cantidad', 1)

        if not producto_id:
            return Response({'detail': 'Producto no especificado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response({'detail': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agregar_producto_al_carrito(usuario_id, producto_id, cantidad)
            return Response({'detail': 'Producto agregado al carrito'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        producto_id = request.data.get('producto_id')
        cantidad     = request.data.get('cantidad', 0)

        if not producto_id:
            return Response({'detail': 'Producto no especificado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response({'detail': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Carrito.objects.get(usuario_id=usuario_id, producto_id=producto_id)
        except Carrito.DoesNotExist:
            return Response({'detail': 'Ítem no existe en el carrito'}, status=status.HTTP_404_NOT_FOUND)

        if cantidad <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        item.cantidad = cantidad
        item.save()
        return Response(CarritoSerializer(item).data, status=status.HTTP_200_OK)

    def delete(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        producto_id = request.data.get('producto_id')
        qs = Carrito.objects.filter(usuario_id=usuario_id)
        if producto_id:
            qs = qs.filter(producto_id=producto_id)

        deleted, _ = qs.delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No se encontró ítem(s) para eliminar'}, status=status.HTTP_404_NOT_FOUND)


class CalcularTotalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'total': calcular_total(usuario_id)}, status=status.HTTP_200_OK)


class RealizarPagoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def post(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        tarjeta_info = request.data.get('tarjeta_info')
        if not tarjeta_info:
            return Response({'detail': 'Info de tarjeta requerida'}, status=status.HTTP_400_BAD_REQUEST)

        resultado = realizar_pago(calcular_total(usuario_id), tarjeta_info)
        if isinstance(resultado, str):
            return Response({'detail': resultado}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Pago realizado con éxito'}, status=status.HTTP_200_OK)


class GenerarReciboView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, usuario_id):
        if request.user.id != usuario_id:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        recibo_data = generar_recibo(usuario_id)
        return Response({'recibo': recibo_data}, status=status.HTTP_200_OK)
