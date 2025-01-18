from django.db import models
from ALC200_asignacion.models.models import CentroComunitario, LEC

class PlanCapacitacion(models.Model):
    centro = models.ForeignKey(CentroComunitario, on_delete=models.CASCADE)
    lecs = models.ManyToManyField(LEC)
    num_sesiones = models.IntegerField()
    modalidad = models.CharField(max_length=50)
    fechas_sesiones = models.JSONField()
    calificaciones = models.JSONField(default=dict)  # Nueva columna para calificaciones
    asistencias = models.JSONField(default=dict)     # Nueva columna para asistencias
    tipo_capacitacion = models.CharField(max_length=50)  # Nuevo campo para tipo de capacitación
    estado = models.BooleanField(default=True) # True Activo, False Inactivo

    def __str__(self):
        return f"Plan de Capacitación para {self.centro}"
