# apps/crm/serializers.py

from rest_framework import serializers
from apps.crm.models import Cliente, Actividad

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono']

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'cliente', 'descripcion', 'fecha_actividad']
