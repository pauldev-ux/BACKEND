# apps/productos/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


from .models import Product
from .serializers import ProductSerializer 
# No necesitamos importar CategorySerializer aquí si no lo usamos directamente

class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para los productos.
    Permite filtrar por ID de categoría, buscar y ordenar.
    """
    queryset = Product.objects.select_related('category').all().order_by('name') # Optimizado y ordenado
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category'] # Permite filtrar por /api/productos/?category=ID
    search_fields = ['name', 'description'] 
    ordering_fields = ['name', 'price', 'stock', 'created_at', 'updated_at']
    ordering = ['name'] 

    @action(detail=True, methods=['post'], url_path='reducir-stock')
    def reduce_stock(self, request, pk=None):
        product = self.get_object()
        try:
            reduce_amount = int(request.data.get('amount', 0))
            if reduce_amount <= 0:
                raise ValueError("La cantidad debe ser positiva.")
        except (TypeError, ValueError) as e:
             return Response({"detail": f"Valor inválido para 'amount': {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock >= reduce_amount:
            product.stock -= reduce_amount
            product.save()
            serializer = self.get_serializer(product) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "No hay suficiente stock.",
                "stock_actual": product.stock 
            }, status=status.HTTP_400_BAD_REQUEST)