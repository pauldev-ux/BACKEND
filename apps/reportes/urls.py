# apps/reportes/urls.py

from django.urls import path
from apps.reportes.views import (
    ReporteListView,
    ReporteDetailView,
    ExportarReportesExcelView,
    ExportarReportesPDFView
)

urlpatterns = [
    path('', ReporteListView.as_view(), name='reportes_list'),             # GET/POST
    path('<int:reporte_id>/', ReporteDetailView.as_view(), name='reporte_detail'),  # GET/PUT/DELETE
    path('export/excel/', ExportarReportesExcelView.as_view(), name='export_excel'),
    path('export/pdf/', ExportarReportesPDFView.as_view(), name='export_pdf'),
]
