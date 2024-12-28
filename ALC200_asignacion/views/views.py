# ALC200_asignacion/views/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.models import LEC

class LECListView(APIView):
    def get(self, request, *args, **kwargs):
        estado = request.query_params.get('estado', None)
        municipio = request.query_params.get('municipio', None)
        localidad = request.query_params.get('localidad', None)

        lecs = LEC.objects.all()

        # Aplicar filtros si los parámetros existen
        if estado:
            lecs = lecs.filter(estado=estado)
        if municipio:
            lecs = lecs.filter(municipio=municipio)
        if localidad:
            lecs = lecs.filter(localidad=localidad)

        # Serializa los datos en formato JSON
        data = [
            {
                "nombre": f"{lec.nombre} {lec.apellido_paterno} {lec.apellido_materno}",
                "estado": lec.estado,
                "municipio": lec.municipio,
                "localidad": lec.localidad
            }
            for lec in lecs
        ]
        return Response(data, status=status.HTTP_200_OK)
