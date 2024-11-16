# serializers.py
from rest_framework import serializers
from ALC000_sistema_base.models.models import Convocatoria

class ConvocatoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'
