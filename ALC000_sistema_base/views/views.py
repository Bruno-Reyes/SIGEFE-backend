# views.py
from rest_framework import viewsets
from ALC000_sistema_base.models.models import Convocatoria
from ALC000_sistema_base.serializers import ConvocatoriaSerializer

class ConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer

