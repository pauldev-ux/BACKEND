# apps/reportes/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated

from apps.reportes.services.reporte_service import (
    create_reporte,
    get_reporte_by_id,
    list_reportes
)
from apps.reportes.serializers import ReporteSerializer

from apps.reportes.exports.excel_exporter import export_to_excel
from apps.reportes.exports.pdf_exporter import export_to_pdf

class ReporteListView(APIView):
    """
    Permite listar todos los reportes o crear un nuevo reporte.
    """
    #permission_classes = [permissions.IsAuthenticated]  # Ajustar a tus necesidades de autenticación

    def get(self, request):
        reportes = list_reportes()
        serializer = ReporteSerializer(reportes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        titulo = request.data.get("titulo")
        descripcion = request.data.get("descripcion", "")
        tipo_reporte = request.data.get("tipo_reporte", "PDF")  # Por defecto 'PDF'
        
        # Tomamos el user_id del usuario que está haciendo la petición
        # (suponiendo que está autenticado)
        user_id = request.user.id  

        if not titulo or not tipo_reporte:
            return Response(
                {"detail": "Faltan campos obligatorios: 'titulo' y/o 'tipo_reporte'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reporte = create_reporte(titulo, descripcion, tipo_reporte, user_id)
        if reporte:
            return Response(
                {"detail": "Reporte creado exitosamente."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail": "Error al crear el reporte. Verifica el usuario."},
                status=status.HTTP_400_BAD_REQUEST
            )

class ReporteDetailView(APIView):
    """
    Permite obtener la información detallada de un reporte o actualizar/eliminar si fuera necesario.
    """
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reporte_id):
        reporte = get_reporte_by_id(reporte_id)
        if not reporte:
            return Response(
                {"detail": "Reporte no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ReporteSerializer(reporte)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Ejemplo de cómo podrías actualizar un reporte
    def put(self, request, reporte_id):
        reporte = get_reporte_by_id(reporte_id)
        if not reporte:
            return Response({"detail": "Reporte no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizamos según los campos que vengan en request.data
        reporte.titulo = request.data.get("titulo", reporte.titulo)
        reporte.descripcion = request.data.get("descripcion", reporte.descripcion)
        reporte.tipo_reporte = request.data.get("tipo_reporte", reporte.tipo_reporte)
        reporte.save()

        return Response({"detail": "Reporte actualizado correctamente."}, status=status.HTTP_200_OK)

    # Ejemplo de cómo podrías eliminar un reporte
    def delete(self, request, reporte_id):
        reporte = get_reporte_by_id(reporte_id)
        if not reporte:
            return Response({"detail": "Reporte no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        reporte.delete()
        return Response({"detail": "Reporte eliminado."}, status=status.HTTP_200_OK)

class ExportarReportesExcelView(APIView):
    """
    Vista para exportar el listado de reportes a un archivo Excel.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        reportes = Reporte.objects.all()  # Puedes aplicar filtros según la lógica de tu aplicación
        return export_to_excel(reportes)

class ExportarReportesPDFView(APIView):
    """
    Vista para exportar el listado de reportes a un archivo PDF.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        reportes = Reporte.objects.all()
        return export_to_pdf(reportes)