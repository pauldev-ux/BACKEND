from django.db import models
from apps.productos.models import Product
from apps.usuarios.models import User

class Carrito(models.Model):
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='carrito_items')
    producto = models.ForeignKey(Product,
                                 on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.name} x{self.cantidad}"
