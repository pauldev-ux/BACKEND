# apps/reportes/views.py

from rest_framework.views      import APIView
from rest_framework.permissions import IsAuthenticated

from apps.ventas.models import Venta
from .exports.sales_excel_exporter import export_sales_to_excel
from .exports.sales_pdf_exporter   import export_sales_to_pdf

class ExportVentasExcelView(APIView):
    """
    GET /api/reportes/ventas/excel/
    → descarga un Excel con el listado de ventas.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Venta.objects.select_related('usuario').order_by('-created_at')
        if not request.user.is_staff and not request.user.is_superuser:
            qs = qs.filter(usuario=request.user)
        return export_sales_to_excel(qs)


class ExportVentasPDFView(APIView):
    """
    GET /api/reportes/ventas/pdf/
    → descarga un PDF con el listado de ventas.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Venta.objects.select_related('usuario').order_by('-created_at')
        if not request.user.is_staff and not request.user.is_superuser:
            qs = qs.filter(usuario=request.user)
        return export_sales_to_pdf(qs)
