from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.utils import timezone
from io import BytesIO
from .models import Reporte
from .serializers import ReporteSerializer
from apps.ventas.models import Venta
from .exports.sales_excel_exporter import export_sales_to_excel
from .exports.sales_pdf_exporter import export_sales_to_pdf

class ReporteListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReporteSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Reporte.objects.all().order_by('-fecha_generado')
        return Reporte.objects.filter(usuario=self.request.user).order_by('-fecha_generado')

class ExportVentasExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Venta.objects.select_related('usuario').order_by('-created_at')
        if not request.user.is_staff and not request.user.is_superuser:
            qs = qs.filter(usuario=request.user)
        return export_sales_to_excel(qs, request.user.id)

class ExportVentasPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Venta.objects.select_related('usuario').order_by('-created_at')
        if not request.user.is_staff and not request.user.is_superuser:
            qs = qs.filter(usuario=request.user)
        return export_sales_to_pdf(qs, request.user.id)