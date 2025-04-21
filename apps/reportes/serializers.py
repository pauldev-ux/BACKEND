# apps/reportes/serializers.py

from rest_framework import serializers
from apps.reportes.models import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    """
    Serializer para manejar la serialización de la información del Reporte.
    """
    class Meta:
        model = Reporte
        fields = ['id', 'titulo', 'descripcion', 'tipo_reporte', 'fecha_generado', 'usuario']
        # 'usuario' aquí es un ForeignKey; si deseas anidar más info, puedes crear un UserSerializer reducido.
