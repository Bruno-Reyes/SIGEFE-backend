# ALC200_asignacion/views/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.models import LEC
from ..models.models import CentroComunitario

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


class CentroComunitarioListView(APIView):
    def get(self, request, *args, **kwargs):
        estado = request.query_params.get('estado', None)
        municipio = request.query_params.get('municipio', None)

        centros = CentroComunitario.objects.all()

        # Aplicar filtros si los parámetros existen
        if estado:
            centros = centros.filter(estado=estado)
        if municipio:
            centros = centros.filter(municipio=municipio)

        # Serializa los datos en formato JSON
        data = [
            {
                "clave_centro_trabajo": centro.clave_centro_trabajo,
                "estado": centro.estado,
                "municipio": centro.municipio,
                "nombre_localidad": centro.nombre_localidad,
                "codigo_postal": centro.codigo_postal,
                "nombre_turno": centro.nombre_turno,
                "nivel_educativo": centro.nivel_educativo,
                "domicilio": centro.domicilio,
                "vacantes": centro.vacantes
            }
            for centro in centros
        ]
        return Response(data, status=status.HTTP_200_OK)