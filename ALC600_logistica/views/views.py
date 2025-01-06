from rest_framework.views import APIView
from rest_framework.response import Response
from ALC600_logistica.models.models import EquipoDisponible, AsignacionMaterial
from ALC600_logistica.serializer import AsignacionMaterialSerializer, EquipoDisponibleSerializer
from rest_framework.decorators import permission_classes
from ALC200_asignacion.models.models import CentroComunitario
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