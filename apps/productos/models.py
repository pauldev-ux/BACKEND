# apps/productos/models.py
from django.db import models
from django.utils import timezone
# --- Importar el modelo Category de la app 'categoria' ---
from apps.categoria.models import Category 

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(verbose_name="Stock")

    # --- Relación con Category (importado) ---
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        db_column='category_id',   
        null=True, 
        blank=True, 
        related_name='products',
        verbose_name="Categoría"
    )

    image_url = models.URLField(max_length=1024, blank=True, null=True, verbose_name="URL de Imagen")

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        db_table = 'productos' 
        ordering = ['name'] 
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name