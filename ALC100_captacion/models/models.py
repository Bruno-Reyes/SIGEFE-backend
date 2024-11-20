from django.db import models

class Convocatoria(models.Model):
    lugar_convocatoria = models.CharField(max_length=50)
    fecha_limite_registro = models.DateField()
    fecha_entrega_resultados = models.DateField()
    max_participantes = models.PositiveIntegerField()
