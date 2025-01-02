from rest_framework import serializers
from ALC600_logistica.models.models import EquipoDisponible

class EquipoDisponibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoDisponible
        fields = '__all__'
