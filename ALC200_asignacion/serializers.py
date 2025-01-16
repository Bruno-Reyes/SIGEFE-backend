from ALC200_asignacion.models.models import CentroComunitario
from rest_framework import serializers

class CentroComunitarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroComunitario
        fields = '__all__'