
from django.urls import path
from .views import ExportVentasExcelView, ExportVentasPDFView, ReporteListView

urlpatterns = [
    path('', ReporteListView.as_view(), name='reporte-list'),
    path('ventas/excel/', ExportVentasExcelView.as_view(), name='export_ventas_excel'),
    path('ventas/pdf/', ExportVentasPDFView.as_view(), name='export_ventas_pdf'),
]
