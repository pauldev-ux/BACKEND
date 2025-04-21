# apps/reportes/exports/pdf_exporter.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import HttpResponse

def export_to_pdf(reportes):
    """
    Genera un archivo PDF a partir de un listado de reportes.
    
    :param reportes: Queryset o lista de objetos Reporte.
    :return: HttpResponse con el archivo PDF para descarga.
    """
    # Creamos un buffer de memoria para almacenar el PDF
    buffer = BytesIO()
    # Inicializamos el canvas con tamaño de página 'letter'
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Posición inicial en el eje Y (de arriba hacia abajo)
    y = height - 50

    # Título del documento
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Reporte de Reportes")
    y -= 30

    # Definir una fuente y tamaño para el contenido
    c.setFont("Helvetica", 12)
    
    # Iterar por cada reporte y escribir sus datos
    for reporte in reportes:
        linea = (
            f"ID: {reporte.id} | Título: {reporte.titulo} | "
            f"Tipo: {reporte.tipo_reporte} | Fecha: {reporte.fecha_generado.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        c.drawString(50, y, linea)
        y -= 20

        # Control de salto de página si el espacio vertical se agota
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50

    c.save()
    buffer.seek(0)

    # Configurar la respuesta HTTP para enviar el PDF
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="reportes.pdf"'
    return response
