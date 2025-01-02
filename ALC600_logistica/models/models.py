from django.db import models

# Modelo para subir equipo disponible

class EquipoDisponible( models.Model ):

    nombre_equipo = models.CharField(max_length=40)
    cantidad_disponible = models.IntegerField()
    descripcion = models.CharField(max_length=360)

    CATEGORIAS = [
        ('Papelería', 'Papelería'),
        ('Utilería', 'Utilería'),
        ('Tecnología', 'Tecnología'),
        ('Mobiliario', 'Mobiliario')
    ]

    categoria = models.CharField( max_length = 18, choices = CATEGORIAS )
