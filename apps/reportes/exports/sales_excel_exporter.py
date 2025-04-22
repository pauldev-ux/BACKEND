
import openpyxl
from openpyxl.workbook import Workbook
from django.http import FileResponse
from django.utils import timezone
from apps.reportes.models import Reporte
import os


def export_sales_to_excel(ventas, user_id):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"
    ws.append(["ID", "Usuario", "Total", "Estado", "Fecha Creación"])

    for v in ventas:
        ws.append([
            v.id,
            v.usuario.username,
            str(v.total),
            v.get_status_display(),
            v.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    filename = f"reporte_ventas_{timezone.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    filepath = os.path.join('media', 'reportes', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    wb.save(filepath)

    Reporte.objects.create(
        titulo="Reporte de ventas (Excel)",
        descripcion="Generado automáticamente",
        tipo_reporte="EXCEL",
        usuario_id=user_id,
        archivo=f"reportes/{filename}"
    )

    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)