from rest_framework import serializers
from ALC300_capacitacion.models.models import PlanCapacitacion

class PlanCapacitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCapacitacion
        fields = '__all__'
