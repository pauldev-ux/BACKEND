# apps/reportes/urls.py

from django.urls import path
from .views import ExportVentasExcelView, ExportVentasPDFView

urlpatterns = [
    path('ventas/excel/', ExportVentasExcelView.as_view(), name='export_ventas_excel'),
    path('ventas/pdf/',   ExportVentasPDFView.as_view(),   name='export_ventas_pdf'),
]
