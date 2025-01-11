from rest_framework import serializers
from ALC500_control_escolar.models.models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'