from rest_framework import viewsets
from ALC500_control_escolar.models.models import Estudiante
from ALC500_control_escolar.serializer import EstudianteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


@permission_classes([AllowAny])
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer