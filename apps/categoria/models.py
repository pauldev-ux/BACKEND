# apps/categoria/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        # Si quieres que Django maneje la tabla (recomendado si no existe):
        # verbose_name = "Categoría"
        # verbose_name_plural = "Categorías"
        # ordering = ['name']
        # Si DEBE usar la tabla 'categorias' existente:
        db_table = 'categorias' 
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name