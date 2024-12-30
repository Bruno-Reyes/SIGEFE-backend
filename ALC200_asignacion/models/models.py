# ALC200_asignacion/models/models.py
from django.db import models

class LEC(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class CentroComunitario(models.Model):
    clave_centro_trabajo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    nombre_localidad = models.CharField(max_length=100) #Municipio
    codigo_postal = models.CharField(max_length=10)
    nombre_turno = models.CharField(max_length=100)
    nivel_educativo = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=255)
    vacantes = models.IntegerField()

    def __str__(self):
        return self.clave_centro_trabajo