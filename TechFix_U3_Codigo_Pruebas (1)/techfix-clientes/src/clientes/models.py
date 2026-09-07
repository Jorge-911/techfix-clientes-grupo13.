from django.db import models

class Cliente(models.Model):
    identificacion = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.identificacion} - {self.nombres}"
