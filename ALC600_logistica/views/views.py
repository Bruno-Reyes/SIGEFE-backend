from rest_framework.views import APIView
from rest_framework.response import Response
from ALC600_logistica.models.models import EquipoDisponible
from ALC600_logistica.serializer import EquipoDisponibleSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class EquipoDisponibleViewSet(ModelViewSet):
    """
    ViewSet para manejar el CRUD de EquipoDisponible
    """
    queryset = EquipoDisponible.objects.all()
    serializer_class = EquipoDisponibleSerializer

@permission_classes([AllowAny])
# Endpoint para obtener todos los equipos disponibles
class EquipoDisponibleListView(APIView):
    def get(self, request):
        equipos = EquipoDisponible.objects.all()
        serializer = EquipoDisponibleSerializer(equipos, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
# Endpoint para crear un nuevo equipo disponible
class EquipoDisponibleCreateView(APIView):
    def post(self, request):
        serializer = EquipoDisponibleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)