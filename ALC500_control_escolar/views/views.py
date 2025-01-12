from rest_framework import viewsets
from ALC500_control_escolar.models.models import Estudiante, Calificaciones
from ALC500_control_escolar.serializer import CalificacionesSerializer, EstudianteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

@permission_classes([AllowAny])
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        queryset = Estudiante.objects.all()
        grado = self.request.query_params.get('grado', None)
        grupo = self.request.query_params.get('grupo', None)
        nivel_educativo = self.request.query_params.get('nivel_educativo', None)
        
        if grado is not None:
            queryset = queryset.filter(grado=grado)
        if grupo is not None:
            queryset = queryset.filter(grupo=grupo)
        if nivel_educativo is not None:
            queryset = queryset.filter(nivel_educativo=nivel_educativo)
        
        return queryset

@permission_classes([AllowAny])
class CalificacionesViewSet(viewsets.ModelViewSet):
    queryset = Calificaciones.objects.all()
    serializer_class = CalificacionesSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = CalificacionesSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Errores de validación:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)