from rest_framework import serializers
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC000_sistema_base.models.models import Usuario

class PagoApoyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoApoyo
        fields = ['id', 'usuario', 'concepto', 'monto', 'fecha_pago', 'estatus', 'registrado_por']
        read_only_fields = ['id', 'fecha_pago']

    def validate_registrado_por(self, value):
        # Verificar si el usuario registrado tiene permiso
        if value != "coord_nac_rrhh@example.com":
            raise serializers.ValidationError("Solo el usuario autorizado puede registrar pagos.")
        return value

