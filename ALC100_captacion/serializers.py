from rest_framework import serializers
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.models.models import DetallesUsuario

class ConvocatoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'  

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'

class DetallesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesUsuario
        fields = '__all__'
