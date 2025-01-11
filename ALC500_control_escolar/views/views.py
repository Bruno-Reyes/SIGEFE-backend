from rest_framework import viewsets
from ALC500_control_escolar.models.models import Estudiante, Calificaciones
from ALC500_control_escolar.serializer import CalificacionesSerializer, EstudianteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


@permission_classes([AllowAny])
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

@permission_classes([AllowAny])
class CalificacionesViewSet(viewsets.ModelViewSet):
    queryset = Calificaciones.objects.all()
    serializer_class = CalificacionesSerializer