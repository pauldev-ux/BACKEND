from rest_framework import serializers
from .models import Cart, CartItem
from apps.productos.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product     = ProductSerializer(read_only=True)
    product_id  = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=ProductSerializer.Meta.model.objects.all(),
        write_only=True
    )

    class Meta:
        model  = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model           = Cart
        fields          = ['id', 'user', 'created_at', 'updated_at', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at']
