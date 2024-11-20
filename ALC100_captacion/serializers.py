from rest_framework import serializers
from ALC100_captacion.models.models import Convocatoria

class CaptacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = '__all__'