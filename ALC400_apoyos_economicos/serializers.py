from rest_framework import serializers
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC000_sistema_base.models.models import Usuario

class PagoApoyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoApoyo
        fields = ['id', 'usuario', 'concepto', 'monto', 'fecha_pago', 'estatus', 'registrado_por', 'confirmacion_lec']
        read_only_fields = ['id', 'fecha_pago']

    def validate(self, data):
        user = self.context['request'].user

        # Validar que solo `coord_nac_rrhh@example.com` puede modificar pagos
        if 'registrado_por' in data and user.email != "coord_nac_rrhh@example.com":
            raise serializers.ValidationError("No tienes permiso para modificar este campo.")

        # Validar que solo `LIDER_LEC` puede modificar `confirmacion_lec`
        if 'confirmacion_lec' in data and user.tipo_usuario != "LIDER_LEC":
            raise serializers.ValidationError("Solo los usuarios LIDER_LEC pueden modificar este campo.")
        
        # Validar que solo `LIDER_LEC` puede modificar `confirmacion_lec`
        if 'estatus' in data and user.email != "dep_finanzas@example.com":
            raise serializers.ValidationError("Solo los usuarios de finanzas pueden modificar este campo.")
        
        return data

