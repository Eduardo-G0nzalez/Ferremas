from django.db import models
from django.utils.text import slugify

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    imagenPrincipal = models.ImageField(upload_to='productos/')
    imagenSecundaria1 = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagenSecundaria2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    caracteristicas = models.TextField(help_text="Separar cada característica con un salto de línea", blank=True, null=True)
    ficha_tecnica = models.FileField(upload_to='fichas/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def obtener_caracteristicas(self):
        """Devuelve la lista de características separadas por salto de línea"""
        return self.caracteristicas.split('\n') if self.caracteristicas else []
