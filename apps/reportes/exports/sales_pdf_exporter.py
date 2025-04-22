# apps/reportes/exports/sales_pdf_exporter.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import HttpResponse

def export_sales_to_pdf(ventas):
    """
    Genera un PDF con:
      ID | Usuario | Total | Estado | Fecha Creación
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Reporte de Ventas")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "ID")
    c.drawString(100, y, "Usuario")
    c.drawString(250, y, "Total")
    c.drawString(330, y, "Estado")
    c.drawString(430, y, "Fecha")
    y -= 20

    c.setFont("Helvetica", 10)
    for v in ventas:
        c.drawString(50, y, str(v.id))
        c.drawString(100, y, v.usuario.username)
        c.drawString(250, y, str(v.total))
        c.drawString(330, y, v.get_status_display())
        c.drawString(430, y, v.created_at.strftime("%Y-%m-%d"))
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ventas.pdf"'
    return response
