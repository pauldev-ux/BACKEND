# apps/productos/serializers.py
from rest_framework import serializers
from .models import Product
# --- Importar Category y CategorySerializer de la app 'categoria' ---
from apps.categoria.models import Category 
from apps.categoria.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    # --- Usar el CategorySerializer importado para la representación anidada ---
    category = CategorySerializer(read_only=True) 

    # Campo para escribir/asignar la categoría por su ID
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), # Obtiene las categorías de su modelo
        source='category', 
        write_only=True,   
        allow_null=True,   
        required=False     
    )

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'stock', 
            'image_url',     
            'category',      # Representación anidada (lectura)
            'category_id',   # Para asignar ID (escritura)
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'category']