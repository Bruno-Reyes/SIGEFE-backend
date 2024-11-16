from django.db import models

# Create your models here.
class Convocatoria(models.Model):
    nombre_convocatoria = models.CharField(max_length=50)
    fecha_registro = models.DateField()
    fecha_entrega_resultados = models.DateField()
    max_participantes = models.PositiveIntegerField()

