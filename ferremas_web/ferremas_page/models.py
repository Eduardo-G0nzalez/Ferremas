from django.db import models
from django.contrib.auth.models import User

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
    stock = models.PositiveIntegerField(default=0, help_text="Cantidad disponible en inventario")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

    def obtener_caracteristicas(self):
        return self.caracteristicas.split('\n') if self.caracteristicas else []
    
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"    
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()  # <--- NUEVO CAMPO
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    orden = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=20, choices=[
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente'),
        ('fallido', 'Fallido'),
    ], default='pagado')

    def __str__(self):
        return f"Compra #{self.id} - Orden {self.orden} - {self.usuario or self.email}"

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
