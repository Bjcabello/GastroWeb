from django.db import models

# Create your models here.
class Menu(models.Model):
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField()
    imagen = models.CharField(max_length=360)
    
    def __str__(self) -> str:
        return self.nombre
    
class Ordenar(models.Model):
    creado = models.DateTimeField(auto_now_add=True)

class OrdenarItem(models.Model):
    ordenar = models.ForeignKey(Ordenar, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)