# apps/carrito/services/carrito_recibo_service.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from apps.carrito.services.carrito_calculo_service import calcular_total
from apps.carrito.models import Carrito

def generar_recibo(usuario_id):
    carrito = Carrito.objects.filter(usuario_id=usuario_id)
    total = calcular_total(usuario_id)
    filename = f"recibo_{usuario_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"Recibo de Compra - Usuario: {usuario_id}")
    y_position = 730
    for item in carrito:
        c.drawString(100, y_position, f"{item.producto.nombre} x{item.cantidad} - ${item.producto.precio}")
        y_position -= 20
    c.drawString(100, y_position, f"Total: ${total}")
    c.save()
    return filename
