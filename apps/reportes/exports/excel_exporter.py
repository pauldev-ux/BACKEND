# apps/reportes/exports/excel_exporter.py

import openpyxl
from openpyxl.workbook import Workbook
from django.http import HttpResponse

def export_to_excel(reportes):
    """
    Genera un archivo Excel (.xlsx) a partir de un listado de reportes.
    
    :param reportes: Queryset o lista de objetos Reporte.
    :return: HttpResponse con el archivo Excel para descarga.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Reportes"
    
    # Definir encabezados
    encabezados = ["ID", "Título", "Descripción", "Tipo de Reporte", "Fecha Generado", "Usuario"]
    ws.append(encabezados)
    
    # Agregar los datos de cada reporte
    for reporte in reportes:
        fila = [
            reporte.id,
            reporte.titulo,
            reporte.descripcion,
            reporte.tipo_reporte,
            reporte.fecha_generado.strftime("%Y-%m-%d %H:%M:%S"),
            reporte.usuario.username  # Asegúrate de que el modelo User tenga el campo 'username'
        ]
        ws.append(fila)
    
    # Preparar la respuesta HTTP con el contenido del archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="reportes.xlsx"'
    
    wb.save(response)
    return response
