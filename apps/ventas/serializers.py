# apps/ventas/serializers.py

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from apps.productos.models import Product
from apps.ventas.models import Venta, VentaDetalle
from apps.usuarios.serializers import UserSerializer

class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        # Usamos el nombre real del campo en el modelo (precio_unitario)
        fields = ['producto_id', 'cantidad', 'precio_unitario']
        extra_kwargs = {
            'cantidad': {'min_value': 1},
            'precio_unitario': {'min_value': 0},
        }

class VentaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    detalles = VentaDetalleSerializer(
        many=True,
        write_only=True,
        help_text="Lista de items: producto_id, cantidad, precio_unitario"
    )
    detalles_info = VentaDetalleSerializer(
        source='detalles',
        many=True,
        read_only=True
    )

    class Meta:
        model = Venta
        fields = [
            'id', 'usuario', 'total', 'status',
            'created_at', 'updated_at',
            'detalles', 'detalles_info',
        ]
        read_only_fields = ['id', 'total', 'status', 'created_at', 'updated_at']

    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError("Debe enviar al menos un item.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        # Calcula el total sumando cantidad × precio_unitario
        total = sum(item['cantidad'] * item['precio_unitario'] for item in detalles_data)
        venta = Venta.objects.create(
            usuario=self.context['request'].user,
            total=total
        )
        # Crea cada detalle y actualiza stock
        for item in detalles_data:
            VentaDetalle.objects.create(
                venta=venta,
                producto_id=item['producto_id'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            )
            Product.objects.filter(id=item['producto_id']) \
                .update(stock=F('stock') - item['cantidad'])
        return venta
