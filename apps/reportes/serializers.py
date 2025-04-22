
from rest_framework import serializers
from .models import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'titulo', 'descripcion', 'tipo_reporte', 'fecha_generado', 'archivo']

