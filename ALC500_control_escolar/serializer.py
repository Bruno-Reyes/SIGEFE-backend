from rest_framework import serializers
from ALC500_control_escolar.models.models import Calificaciones, Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class CalificacionesSerializer(serializers.ModelSerializer):
    promedio = serializers.FloatField()

    class Meta:
        model = Calificaciones
        fields = '__all__'