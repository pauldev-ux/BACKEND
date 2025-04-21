# apps/ventas/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.ventas.models import Venta
from apps.ventas.services.checkout_service import checkout_usuario
from apps.ventas.serializers import VentaSerializer

class VentaViewSet(viewsets.ModelViewSet):
    """
    list, retrieve, create, update (sin nested-details), destroy.
    """
    queryset = Venta.objects.prefetch_related('detalles').all().order_by('-created_at')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return self.queryset
        return self.queryset.filter(usuario=user)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario_id = request.user.id
        try:
            venta = checkout_usuario(usuario_id)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VentaSerializer(venta, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
