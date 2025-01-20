from rest_framework.views import APIView
from rest_framework.response import Response
from ALC600_logistica.models.models import EquipoDisponible, AsignacionMaterial, CentrosDistribucion
from ALC600_logistica.serializer import AsignacionMaterialSerializer, EquipoDisponibleSerializer, CentroDistribucionSerializer
from ALC200_asignacion.serializers import CentroComunitarioSerializer    
from rest_framework.decorators import permission_classes
from ALC200_asignacion.models.models import CentroComunitario
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ALC600_logistica.services import solve_cvrp
from rest_framework import status

import json


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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@permission_classes([AllowAny])
class CrearAsignacionView(APIView):
    def post(self, request):

        try:

            # Obtener equipo y centro comunitario
            equipo = EquipoDisponible.objects.get(id=request.data.get("equipo_id"))
            centro = CentroComunitario.objects.get(id=request.data.get("centro_id"))

            # Validar cantidad
            cantidad = int(request.data.get("cantidad_asignada"))
            if cantidad <= 0 or cantidad > equipo.cantidad_disponible:
                return Response(
                    {"error": "La cantidad no es válida o supera la cantidad disponible."},
                )

            # Crear la asignación
            asignacion = AsignacionMaterial.objects.create(
                equipo=equipo,
                centro_id=centro.id,
                cantidad_asignada=cantidad,
            )

            # Reducir la cantidad disponible del equipo
            equipo.cantidad_disponible -= cantidad
            equipo.save()

            # Serializar la asignación
            serializer = AsignacionMaterialSerializer(asignacion)

            return Response(serializer.data)

        except EquipoDisponible.DoesNotExist:
            return Response({"error": f"El equipo seleccionado no existe."})
        except CentroComunitario.DoesNotExist:
            return Response({"error": "El centro seleccionado no existe."})
        except Exception as e:
            return Response({"error": str(e)})
        
        
@permission_classes([AllowAny])
class AsignacionListView(APIView):
    def get(self, request):
        try:
            asignaciones = AsignacionMaterial.objects.all()
            if not asignaciones.exists():
                return Response({"message": "No hay asignaciones registradas."}, status=200)

            serializer = AsignacionMaterialSerializer(asignaciones, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": f"Error interno: {str(e)}"}, status=500)
        
@permission_classes([AllowAny])
class ConsultarEstados(APIView):
    def get(self, request):
        try: 
            estados = CentroComunitario.objects.values_list('estado', flat=True).distinct()
            return Response({"estados": list(estados)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
@permission_classes([AllowAny])
class GenerarRuta(APIView):
    def post(self, request): 
        try:
            # Obtener el estado
            data = json.loads(request.body)
            estado = data.get("estado")
                    
            if not estado:
                return Response({"error": "El estado es requerido."}, status=400)
            # Obtener el centro de distribución del estado
            centro_distribucion = CentrosDistribucion.objects.filter(estado__exact=estado)
            # Verificar si hay resultados
            if not centro_distribucion.exists():
                return Response({"error": "No se encontraron centros de distribución para el estado proporcionado."},
                                status=status.HTTP_404_NOT_FOUND)

            # Serializar los resultados
            serializer_centro_distribucion = CentroDistribucionSerializer(centro_distribucion, many=True)
            # Obtener los centros comunitarios del estado
            centros = CentroComunitario.objects.filter(estado__exact=estado)
            if not centros.exists():
                return Response({"message": "No hay centros comunitarios registrados en el estado."}, status=200)
            serializer_centros_comunitarios = CentroComunitarioSerializer(centros, many=True)
            # Obtener las asignaciones de los centros
            asignaciones = AsignacionMaterial.objects.filter(centro__in=centros)
            if not asignaciones.exists():
                return Response({"message": "No hay asignaciones registradas en los centros del estado."}, status=200)
            
            # Generar la ruta
            route, cost = solve_cvrp(centro_distribucion, centros)

            return Response({"centro_distribucion": serializer_centro_distribucion.data,
                             "localidades" : serializer_centros_comunitarios.data, 
                             "ruta_distribucion" : route,
                             "cost" : cost}, status=200)
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
@permission_classes([IsAuthenticated])
class CentrosPorEstadoAPIView(APIView):
    def get(self, request, estado):
        # Obtener centros comunitarios por estado
        centros = CentroComunitario.objects.filter(estado=estado).values("clave_centro_trabajo", "latitud", "longitud")
        
        # Obtener el centro de distribución del estado
        centro_distribucion = CentrosDistribucion.objects.filter(estado=estado).values("latitud", "longitud").first()
        
        if not centros.exists() or not centro_distribucion:
            return Response({"error": "No se encontraron datos para el estado proporcionado"}, status=404)
        
        return Response({
            "centros_comunitarios": list(centros),
            "centro_distribucion": centro_distribucion
        })