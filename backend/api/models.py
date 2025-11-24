# models.py
from django.db import models

class Ubicacion(models.Model):
    nombre_ubicacion = models.CharField(max_length=100) # [cite: 306]
    # Simplificamos departamento por ahora para el boilerplate

    def __str__(self):
        return self.nombre_ubicacion

class Activo(models.Model):
    # Estados definidos en el negocio
    ESTADOS = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENCION', 'En Mantención'),
        ('BAJA', 'De Baja'),
    ]

    # Campos exactos del diagrama [cite: 320-324]
    codigo_inventario = models.CharField(max_length=50, unique=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='OPERATIVO')

    # Relación: Un activo está en una ubicación actual [cite: 325]
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.modelo} - {self.codigo_inventario}"