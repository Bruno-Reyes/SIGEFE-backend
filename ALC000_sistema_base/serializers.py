from django.contrib.auth import authenticate
from rest_framework import serializers
from ALC000_sistema_base.models.models import Usuario
from ALC400_apoyos_economicos.models.models import ALC004TiposBecas

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        # Obtenemos el tipo de usuario
        if user is None:
            raise serializers.ValidationError("Las credenciales son incorrectas.")
        elif user.tipo_usuario == 'aspirante_lec':
            raise serializers.ValidationError("Solo puedes iniciar sesión si fuiste asignado en un centro comunitario.")
        
        

        data['user'] = user
        return data

class UsuarioSerializer(serializers.ModelSerializer):
    tipo_beca_asignada = serializers.CharField(default=None)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'tipo_usuario', 'is_active', 'date_joined', 'tipo_beca_asignada']