# ALC200_asignacion/views/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.models import LEC, CentroComunitario

class LECListView(APIView):
    def get(self, request, *args, **kwargs):
        estado = request.query_params.get('estado', None)
        municipio = request.query_params.get('municipio', None)
        localidad = request.query_params.get('localidad', None)
        centro_asignado = request.query_params.get('centro_asignado', None)

        lecs = LEC.objects.all()

        # Aplicar filtros si los parámetros existen
        if estado:
            lecs = lecs.filter(estado=estado)
        if municipio:
            lecs = lecs.filter(municipio=municipio)
        if localidad:
            lecs = lecs.filter(localidad=localidad)
        if centro_asignado:
            lecs = lecs.filter(centro_asignado_id=centro_asignado)

        # Serializa los datos en formato JSON
        data = [
            {
                "id": lec.id,
                "nombre": f"{lec.nombre} {lec.apellido_paterno} {lec.apellido_materno}",
                "estado": lec.estado,
                "municipio": lec.municipio,
                "localidad": lec.localidad,
                "centro_asignado": lec.centro_asignado.clave_centro_trabajo if lec.centro_asignado else None,
                "cct_centro_asignado": lec.cct_centro_asignado if lec.centro_asignado else None,
                "estado_centro_asignado": lec.estado_centro_asignado if lec.centro_asignado else None,
                "municipio_centro_asignado": lec.municipio_centro_asignado if lec.centro_asignado else None
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
                "id": centro.id,
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
    
class AsignarCentroLEC(APIView):
    def post(self, request):
        lec_id = request.data.get("lec_id")
        centro_id = request.data.get("centro_id")

        if not lec_id:
            return Response(
                {"error": "Se requieren lec_id."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not centro_id:
            return Response(
                {"error": "Se requieren centro_id."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lec = LEC.objects.get(id=lec_id)
            centro = CentroComunitario.objects.get(id=centro_id)
            

            # Verificar que el centro tiene vacantes disponibles
            if centro.vacantes <= 0:
                return Response(
                    {"error": "El centro no tiene vacantes disponibles."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Asignar el centro al LEC
            lec.centro_asignado = centro
            lec.cct_centro_asignado = centro.clave_centro_trabajo
            lec.estado_centro_asignado = centro.estado
            lec.municipio_centro_asignado = centro.municipio
            lec.save()

            # Reducir las vacantes del centro
            centro.vacantes -= 1
            centro.save()

            return Response(
                {"message": f"LEC {lec.nombre} asignado al centro {centro.clave_centro_trabajo} exitosamente."},
                status=status.HTTP_200_OK
            )

        except LEC.DoesNotExist:
            return Response({"error": "LEC no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except CentroComunitario.DoesNotExist:
            return Response({"error": "Centro comunitario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EliminarLECView(APIView):
    def delete(self, request, lec_id):
        try:
            lec = LEC.objects.get(id=lec_id)
            centro = lec.centro_asignado

            if centro:
                # Incrementar las vacantes del centro
                centro.vacantes += 1
                centro.save()

            # Eliminar la asignación del LEC
            lec.centro_asignado = None
            lec.cct_centro_asignado = None
            lec.estado_centro_asignado = None
            lec.municipio_centro_asignado = None
            lec.save()

            return Response({"message": "LEC eliminado correctamente."}, status=status.HTTP_200_OK)
        except LEC.DoesNotExist:
            return Response({"error": "LEC no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)