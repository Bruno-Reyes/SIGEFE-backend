from rest_framework import viewsets
from ALC500_control_escolar.models.models import Estudiante, Calificaciones
from ALC500_control_escolar.serializer import CalificacionesSerializer, EstudianteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from ALC200_asignacion.models.models import HistorialAsignacion, CentroComunitario
from django.db import models

@permission_classes([AllowAny])
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        queryset = Estudiante.objects.all()
        grado = self.request.query_params.get('grado', None)
        grupo = self.request.query_params.get('grupo', None)
        nivel_educativo = self.request.query_params.get('nivel_educativo', None)
        nombre = self.request.query_params.get('nombre', None)
        apellido_paterno = self.request.query_params.get('apellido_paterno', None)
        apellido_materno = self.request.query_params.get('apellido_materno', None)
        
        if grado is not None:
            queryset = queryset.filter(grado=grado)
        if grupo is not None:
            queryset = queryset.filter(grupo=grupo)
        if nivel_educativo is not None:
            queryset = queryset.filter(nivel_educativo=nivel_educativo)
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if apellido_paterno is not None:
            queryset = queryset.filter(apellido_paterno__icontains=apellido_paterno)
        if apellido_materno is not None:
            queryset = queryset.filter(apellido_materno__icontains=apellido_materno)
        
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

@permission_classes([AllowAny])
class HistorialMigratorioViewSet(viewsets.ViewSet):
    def list(self, request):
        nombre = request.query_params.get('nombre', None)
        if nombre:
            estudiantes = Estudiante.objects.filter(nombre__icontains=nombre)
            historial = []
            for estudiante in estudiantes:
                asignaciones = HistorialAsignacion.objects.filter(lec__nombre=estudiante.nombre)
                for asignacion in asignaciones:
                    centro = asignacion.centro
                    historial.append({
                        'cct': centro.clave_centro_trabajo,
                        'estado': centro.estado,
                        'municipio': centro.municipio,
                        'localidad': centro.nombre_localidad,
                    })
            return Response(historial, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)