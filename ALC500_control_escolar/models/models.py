from django.db import models

class Estudiante(models.Model):

    id_lec = models.IntegerField()
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    edad = models.IntegerField()
    grado = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)
    promedio_global = models.DecimalField(max_digits=4, decimal_places=2)
    centro_educativo = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    nivel_educativo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} - {self.centro_educativo}"
    

class Calificaciones(models.Model):

    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)
    grado = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)
    bimestre = models.IntegerField()

    def __str__(self):
        return f"{self.materia} - {self.calificacion}"