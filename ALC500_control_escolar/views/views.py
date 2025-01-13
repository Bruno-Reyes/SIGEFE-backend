from rest_framework import viewsets
from ALC500_control_escolar.models.models import Estudiante, Calificaciones
from ALC500_control_escolar.serializer import CalificacionesSerializer, EstudianteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import models
from rest_framework.views import APIView
from ALC500_control_escolar.models.models import HistorialMigratorio
import requests
from django.conf import settings

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

    def get_queryset(self):
        queryset = Calificaciones.objects.all()
        id_estudiante = self.request.query_params.get('id_estudiante__in', None)
        
        if id_estudiante is not None:
            id_estudiante_list = id_estudiante.split(',')
            queryset = queryset.filter(id_estudiante__in=id_estudiante_list)
        
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        email = request.data[0].get('email')  # Obtener el email del primer elemento de la lista
        print(email)
        if not email:
            return Response({"error": "Se requiere email."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el token de acceso del encabezado de la solicitud
        token = request.headers.get('Authorization').split(' ')[1]

        # Obtener el CCT del LEC
        lec_response = requests.get(f"{settings.API_URL}/asignacion/lecs?email={email}", headers={"Authorization": f"Bearer {token}"})
        if lec_response.status_code != 200:
            return Response({"error": "No se pudo obtener el CCT del LEC."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        lec_data = lec_response.json()[0]  # Acceder al primer elemento del array
        cct_centro_asignado = lec_data.get('cct_centro_asignado')
        print(f"CCT del LEC: {cct_centro_asignado}")

        # Verificar si el LEC tiene control sobre los estudiantes
        estudiantes_ids = [calificacion['id_estudiante'] for calificacion in request.data]
        estudiantes = Estudiante.objects.filter(id__in=estudiantes_ids)

        # Filtrar estudiantes por grado, grupo y nivel educativo
        grado = request.data[0].get('grado')
        grupo = request.data[0].get('grupo')
        nivel_educativo = request.data[0].get('nivel_educativo')
        estudiantes = estudiantes.filter(grado=grado, grupo=grupo, nivel_educativo=nivel_educativo)

        for estudiante in estudiantes:
            print(f"Estudiante ID: {estudiante.id}, Centro Educativo: {estudiante.centro_educativo}")
            if estudiante.centro_educativo != cct_centro_asignado:
                return Response({"error": f"El LEC no tiene control sobre el estudiante {estudiante.id}."}, status=status.HTTP_403_FORBIDDEN)

        for calificacion_data in request.data:
            id_estudiante = calificacion_data['id_estudiante']
            materia = calificacion_data['materia']
            bimestre = calificacion_data['bimestre']

            # Buscar si ya existe una calificación para el mismo estudiante, materia y bimestre
            calificacion_existente = Calificaciones.objects.filter(
                id_estudiante=id_estudiante,
                materia=materia,
                bimestre=bimestre
            ).first()

            if calificacion_existente:
                # Si existe, actualizar la calificación
                calificacion_existente.calificacion = calificacion_data['calificacion']
                calificacion_existente.promedio = calificacion_data['promedio']
                calificacion_existente.save()
            else:
                # Si no existe, crear una nueva calificación
                serializer = CalificacionesSerializer(data=calificacion_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print("Errores de validación:", serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Calificaciones registradas correctamente."}, status=status.HTTP_201_CREATED)

class HistorialMigratorioView(APIView):
    def post(self, request):
        id_estudiante = request.data.get('id_estudiante')
        fecha_inscripcion = request.data.get('fecha_inscripcion')
        clave_centro_trabajo = request.data.get('clave_centro_trabajo')
        email = request.data.get('email')
        
        # Imprimir los parámetros recibidos
        print(f"Parametros recibidos - id_estudiante: {id_estudiante}, fecha_inscripcion: {fecha_inscripcion}, clave_centro_trabajo: {clave_centro_trabajo}, email: {email}")

        if not email:
            return Response({"error": "Se requiere email."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener el token de acceso del encabezado de la solicitud
            token = request.headers.get('Authorization').split(' ')[1]

            # Obtener el CCT del LEC
            lec_response = requests.get(f"{settings.API_URL}/asignacion/lecs?email={email}", headers={"Authorization": f"Bearer {token}"})
            if lec_response.status_code != 200:
                return Response({"error": "No se pudo obtener el CCT del LEC."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            lec_data = lec_response.json()
            if not lec_data:
                return Response({"error": "No se encontró el email en la base de datos."}, status=status.HTTP_404_NOT_FOUND)
            
            lec_data = lec_data[0]  # Acceder al primer elemento del array
            cct_centro_asignado = lec_data.get('cct_centro_asignado')
            print(f"CCT del LEC: {cct_centro_asignado}")
            # Verificar si el LEC tiene control sobre el estudiante
            estudiante = Estudiante.objects.get(id=id_estudiante)
            print(f"Estudiante ID: {estudiante.id}, Centro Educativo: {estudiante.centro_educativo}")
            if estudiante.centro_educativo != cct_centro_asignado:
                return Response({"error": "El LEC no tiene control sobre este estudiante."}, status=status.HTTP_403_FORBIDDEN)

            # Convertir la fecha de inscripción al formato correcto
            fecha_inscripcion = fecha_inscripcion.split('T')[0]
            print(f"Registrando historial migratorio - id_estudiante: {id_estudiante}, fecha_inscripcion: {fecha_inscripcion}, clave_centro_trabajo: {clave_centro_trabajo}")
            historial = HistorialMigratorio.objects.create(
                id_estudiante_id=id_estudiante,
                fecha_inscripcion=fecha_inscripcion,
                clave_centro_trabajo=clave_centro_trabajo
            )
            historial.save()

            # Actualizar el campo centro_educativo del estudiante
            estudiante.centro_educativo = clave_centro_trabajo
            estudiante.save()

            print("Historial migratorio registrado y centro educativo actualizado correctamente")
            return Response({"message": "Historial migratorio registrado y centro educativo actualizado correctamente."}, status=status.HTTP_201_CREATED)
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
