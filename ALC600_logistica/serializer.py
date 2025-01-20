from rest_framework import serializers
from ALC600_logistica.models.models import EquipoDisponible, AsignacionMaterial, CentrosDistribucion

class EquipoDisponibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoDisponible
        fields = '__all__'

class AsignacionMaterialSerializer(serializers.ModelSerializer):
    nombre_equipo = serializers.CharField(source='equipo.nombre_equipo', read_only=True)
    categoria = serializers.CharField(source='equipo.categoria', read_only=True)
    clave_centro_trabajo = serializers.CharField(source='centro.clave_centro_trabajo', read_only=True)
    estado = serializers.CharField(source='centro.estado', read_only=True)
    municipio = serializers.CharField(source='centro.municipio', read_only=True)
    cantidad = serializers.IntegerField(source='cantidad_asignada', read_only=True)

    class Meta:
        model = AsignacionMaterial
        fields = [
            'id',
            'cantidad',
            'nombre_equipo',
            'categoria',
            'clave_centro_trabajo',
            'estado',
            'municipio',
        ]
        
class CentroDistribucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentrosDistribucion
        fields = '__all__' 