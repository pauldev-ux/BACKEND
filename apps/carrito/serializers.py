from rest_framework import serializers
from .models import Carrito

class CarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.name', read_only=True)
    producto_precio = serializers.DecimalField(
        source='producto.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Carrito
        fields = [
            'id',
            'usuario',
            'producto',
            'producto_nombre',
            'producto_precio',
            'cantidad',
            'fecha_agregado'
        ]
        read_only_fields = ['fecha_agregado']
