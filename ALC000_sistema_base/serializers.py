from django.contrib.auth import authenticate
from rest_framework import serializers

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
