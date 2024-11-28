# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.serializers import ConvocatoriaSerializer
from django.utils import timezone

class ConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer

# Endpoint para obtener la lista de convocatorias activas
# GET /api/convocatorias/activas/
class ConvocatoriasActivas(APIView):
    def get(self, request):
        fecha_actual = timezone.now().date()
        convocatorias = Convocatoria.objects.filter(fecha_limite_registro__gte=fecha_actual)
        serializer = ConvocatoriaSerializer(convocatorias, many=True)
        return Response(serializer.data)