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
from rest_framework.views import APIView
from ALC500_control_escolar.models.models import HistorialMigratorio

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

class HistorialMigratorioView(APIView):
    def post(self, request):
        id_estudiante = request.data.get('id_estudiante')
        fecha_inscripcion = request.data.get('fecha_inscripcion')
        clave_centro_trabajo = request.data.get('clave_centro_trabajo')

        try:
            # Convertir la fecha de inscripción al formato correcto
            fecha_inscripcion = fecha_inscripcion.split('T')[0]
            print(f"Registrando historial migratorio - id_estudiante: {id_estudiante}, fecha_inscripcion: {fecha_inscripcion}, clave_centro_trabajo: {clave_centro_trabajo}")
            historial = HistorialMigratorio.objects.create(
                id_estudiante_id=id_estudiante,
                fecha_inscripcion=fecha_inscripcion,
                clave_centro_trabajo=clave_centro_trabajo
            )
            historial.save()
            print("Historial migratorio registrado correctamente")
            return Response({"message": "Historial migratorio registrado correctamente."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error al registrar el historial migratorio: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        id_estudiante = request.query_params.get('id_estudiante')
        if not id_estudiante:
            print("Error: Se requiere id_estudiante.")
            return Response({"error": "Se requiere id_estudiante."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(f"Obteniendo historial migratorio para id_estudiante: {id_estudiante}")
            historial = HistorialMigratorio.objects.filter(id_estudiante_id=id_estudiante)
            if not historial.exists():
                print(f"No se encontró historial migratorio para id_estudiante: {id_estudiante}")
            else:
                print(f"Historial migratorio encontrado para id_estudiante: {id_estudiante}")
            data = [
                {
                    "id_estudiante": item.id_estudiante_id,
                    "fecha_inscripcion": item.fecha_inscripcion,
                    "clave_centro_trabajo": item.clave_centro_trabajo
                }
                for item in historial
            ]
            print(f"Historial migratorio obtenido: {data}")
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error al obtener el historial migratorio: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
