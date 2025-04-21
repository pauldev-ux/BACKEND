# apps/carrito/serializers.py
from rest_framework import serializers
from apps.carrito.models import Carrito
from apps.productos.models import Producto

class CarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre')
    producto_precio = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2)
    
    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'producto', 'producto_nombre', 'producto_precio', 'cantidad', 'fecha_agregado']
