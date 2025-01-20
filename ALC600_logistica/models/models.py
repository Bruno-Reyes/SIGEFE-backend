from django.db import models
from ALC200_asignacion.models.models import CentroComunitario

# Modelo para subir equipo disponible

class EquipoDisponible( models.Model ):
    nombre_equipo = models.CharField(max_length=40)
    cantidad_disponible = models.IntegerField()
    descripcion = models.CharField(max_length=360)

    CATEGORIAS = [
        ('Papelería', 'Papelería'),
        ('Utilería', 'Utilería'),
        ('Mobiliario', 'Mobiliario'),
        ('Ropa y Calzado', 'Ropa y Calzado'),
    ]

    categoria = models.CharField( max_length = 18, choices = CATEGORIAS )
    volumen = models.FloatField(blank=True, null=True)
    def __str__(self):
        return f"Nombre equipo: {self.nombre_equipo}\nCantidad disponible: {self.cantidad_disponible} \n"

class AsignacionMaterial(models.Model):
    equipo = models.ForeignKey(EquipoDisponible, on_delete=models.CASCADE, related_name='asignaciones')
    centro = models.ForeignKey(CentroComunitario, on_delete=models.CASCADE, related_name='asignaciones')
    cantidad_asignada = models.PositiveIntegerField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad_asignada} x {self.equipo.nombre_equipo} -> {self.centro.clave_centro_trabajo}"

class CentrosDistribucion(models.Model): 
    estado = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)    
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)