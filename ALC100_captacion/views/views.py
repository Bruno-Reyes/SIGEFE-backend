# views.py
from rest_framework import viewsets
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.serializers import ConvocatoriaSerializer

class ConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer