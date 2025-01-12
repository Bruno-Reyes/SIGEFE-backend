from rest_framework import serializers
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC000_sistema_base.models.models import Usuario
from ALC400_apoyos_economicos.models.models import ALC004TiposBecas
from ALC400_apoyos_economicos.models.models import ALC401LecBecas

class PagoApoyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoApoyo
        fields = ['id', 'usuario', 'concepto', 'monto', 'fecha_pago', 'estatus', 'registrado_por', 'confirmacion_lec']
        read_only_fields = ['id', 'fecha_pago']

    def validate(self, data):
        user = self.context['request'].user

        # Validar que solo `coord_nac_rrhh@example.com` puede registrar pagos
        if 'registrado_por' in data and user.email != "coord_nac_rrhh@example.com":
            raise serializers.ValidationError("No tienes permiso para modificar el campo 'registrado_por'.")

        # Validar que solo los usuarios `LIDER_LEC` pueden modificar `confirmacion_lec`
        if 'confirmacion_lec' in data and user.tipo_usuario != "LIDER_LEC":
            raise serializers.ValidationError("Solo los usuarios LIDER_LEC pueden modificar este campo.")

        # Validar que el monto sea mayor a 0
        if 'monto' in data and data['monto'] <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")

        return data

    
class ALC004TiposBecasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALC004TiposBecas
        fields = ['id', 'tipo', 'monto']

class ALC401LecBecasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALC401LecBecas
        fields = ['id', 'tipo_beca', 'usuario', 'estatus']
        
    # Validación adicional para asegurarse de que no se asignen becas duplicadas
    def validate(self, data):
        if ALC401LecBecas.objects.filter(tipo_beca=data['tipo_beca'], usuario=data['usuario']).exists():
            raise serializers.ValidationError("El usuario ya tiene esta beca asignada.")
        return data
    
class UsuarioConBecaSerializer(serializers.ModelSerializer):
    tipo_beca_asignada = serializers.CharField()

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'tipo_usuario', 'tipo_beca_asignada']

class LecBecasSerializer(serializers.ModelSerializer):
    tipo_beca = ALC004TiposBecasSerializer()  # Relación con TiposBecas

    class Meta:
        model = ALC401LecBecas
        fields = ['id', 'usuario', 'tipo_beca', 'estatus']
