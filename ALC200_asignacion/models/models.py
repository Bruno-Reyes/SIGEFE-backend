# ALC200_asignacion/models/models.py
from django.db import models
from django.utils import timezone

class LEC(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    centro_asignado = models.ForeignKey('CentroComunitario', on_delete=models.SET_NULL, null=True, blank=True)
    cct_centro_asignado = models.CharField(max_length=100, null=True, blank=True)
    estado_centro_asignado = models.CharField(max_length=100, null=True, blank=True)
    municipio_centro_asignado = models.CharField(max_length=100, null=True, blank=True)
    fecha_asignacion = models.DateTimeField(default=timezone.now)  # Registrar automáticamente la fecha de asignación
    email = models.EmailField(max_length=254, unique=True)  # No permitir valores nulos

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class CentroComunitario(models.Model):
    clave_centro_trabajo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    nombre_localidad = models.CharField(max_length=100) #Municipio
    codigo_postal = models.CharField(max_length=10)
    nombre_turno = models.CharField(max_length=100)
    nivel_educativo = models.CharField(max_length=100)  # Corregir a max_length
    domicilio = models.CharField(max_length=255)
    vacantes = models.IntegerField()

    def __str__(self):
        return self.clave_centro_trabajo

class HistorialAsignacion(models.Model):
    lec = models.ForeignKey(LEC, on_delete=models.CASCADE)
    centro = models.ForeignKey(CentroComunitario, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.lec} asignado a {self.centro} el {self.fecha_asignacion}"