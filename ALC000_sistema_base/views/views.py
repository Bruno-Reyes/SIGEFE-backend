from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ALC000_sistema_base.serializers import CustomAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ALC000_sistema_base.models.models import Usuario
from ALC000_sistema_base.serializers import UsuarioSerializer
from ALC000_sistema_base.serializers import UsersSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomAuthTokenSerializer

class ObtainCustomTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Agregar información personalizada al payload
            payload = {
                'email': user.email,
                'tipo_usuario': user.tipo_usuario,
                'exp': access_token.payload['exp'],
            }

            # Enviar el token y la información personalizada
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'payload': payload
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LiderLecListView(APIView):
    def get(self, request):
        # Filtrar los usuarios cuyo tipo_usuario sea 'lider_lec'
        lideres = Usuario.objects.filter(tipo_usuario='lider_lec')
        serializer = UsuarioSerializer(lideres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LecListView(APIView):
    def get(self, request):
        # Filtrar los usuarios cuyo tipo_usuario sea 'lider_lec'
        lideres = Usuario.objects.filter(tipo_usuario='lider_lec')
        serializer = UsersSerializer(lideres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
