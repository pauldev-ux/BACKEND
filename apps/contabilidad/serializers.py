# apps/contabilidad/serializers.py

from rest_framework import serializers
from apps.contabilidad.models import Cuenta, Transaccion

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['id', 'nombre_cuenta', 'tipo_cuenta', 'created_at']

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = ['id', 'cuenta', 'monto', 'descripcion', 'fecha_transaccion']
