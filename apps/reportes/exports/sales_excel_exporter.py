# apps/reportes/exports/sales_excel_exporter.py

import openpyxl
from openpyxl.workbook import Workbook
from django.http import HttpResponse

def export_sales_to_excel(ventas):
    """
    Genera un Excel (.xlsx) con:
      ID | Usuario | Total | Estado | Fecha Creación
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    # Encabezados
    ws.append(["ID", "Usuario", "Total", "Estado", "Fecha Creación"])

    for v in ventas:
        ws.append([
            v.id,
            v.usuario.username,
            str(v.total),
            v.get_status_display(),
            v.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="ventas.xlsx"'
    wb.save(response)
    return response
