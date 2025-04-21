# apps/voz/serializers.py

from rest_framework import serializers
from apps.voz.models import VozComando

class VozComandoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VozComando
        fields = ['id', 'usuario', 'comando_recibido', 'resultado_accion', 'fecha_comando']
        # Opcional: para mostrar datos de usuario anidados, podrías usar un UserSerializer o depth=1
        # depth = 1
