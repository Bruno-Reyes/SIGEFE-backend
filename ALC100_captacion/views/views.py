# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.serializers import ConvocatoriaSerializer
from ALC100_captacion.serializers import DetallesUsuarioSerializer
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from ALC100_captacion.services import subir_archivo_azure
from ALC000_sistema_base.services import enviar_email
from ALC200_asignacion.models.models import LEC
from django.db import models
import json



# Provisional
from ALC000_sistema_base.models.models import Usuario
from ALC100_captacion.models.models import DetallesUsuario
from ALC100_captacion.models.models import Inscripciones
from ALC000_sistema_base.models.models import TipoUsuario
from services.send_mail import authenticate, send_mail
from services.generate_azure_sas_url import generate_sas_url
from utils.mensajes_predefinidos import mensaje_registro_exitoso, mensaje_aceptacion, mensaje_rechazo


class ConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer

# Endpoint para obtener la lista de convocatorias activas
# GET /api/convocatorias/activas/


class ConvocatoriasActivas(APIView):
    def get(self, request):
        fecha_actual = timezone.now().date()
        convocatorias = Convocatoria.objects.filter(
            fecha_limite_registro__gte=fecha_actual)
        serializer = ConvocatoriaSerializer(convocatorias, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class ObtenerActivas(APIView):
    def get(self, request):
        fecha_actual = timezone.now().date()
        convocatorias = Convocatoria.objects.filter(
            fecha_limite_registro__gte=fecha_actual)
        serializer = ConvocatoriaSerializer(convocatorias, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class RegistrarCandidato(APIView):
    def post(self, request):
        values = json.loads(request.data.get("data"))

        # Validar un único correo desde servidor
        usuario = Usuario.objects.filter(email=values["correo"])
        if usuario:
            return Response({"detail": "El correo ya ha sido registrado"}, status=400)
        else:
            # Extraer los archivos y guardarlos en Azure
            fichero_certificado = request.data.get("files[0]")
            fichero_identificacion = request.data.get("files[1]")
            fichero_estado_cuenta = request.data.get("files[2]")

            # Subir archivos a Azure
            certificado_url = subir_archivo_azure(
                fichero_certificado, "certificados")
            identificacion_url = subir_archivo_azure(
                fichero_identificacion, "identificaciones")
            estado_cuenta_url = subir_archivo_azure(
                fichero_estado_cuenta, "cuentas")

            if not certificado_url or not identificacion_url or not estado_cuenta_url:
                return Response({"detail": "Error al subir archivos"}, status=400)
            else:
                # Crear un usuario con datos sintéticos
                usuario = Usuario.objects.create_user(
                    email=values["correo"],
                    password=values["contrasena"],
                    tipo_usuario=TipoUsuario.ASPIRANTE_LEC,
                )

                # Crear un candidato con datos sintéticos
                detallesUsuario = DetallesUsuario.objects.create(
                    usuario=usuario,
                    curp=values["curp"],
                    nombres=values["nombres"],
                    apellido_paterno=values["apellido_paterno"],
                    apellido_materno=values["apellido_materno"],
                    fecha_nacimiento=values["fecha_nacimiento"].split("T")[0],
                    genero=values["genero"],
                    talla_playera=values["talla_playera"],
                    talla_pantalon=values["talla_pantalon"],
                    talla_calzado=values["talla_calzado"],
                    peso=values["peso"],
                    estatura=values["estatura"],
                    afecciones=values["afecciones"],
                    banco=values["banco"],
                    clabe=values["clabe"],
                    nivel_estudios=values["nivel_estudios"],
                    nivel_estudios_deseado=values["nivel_estudios_deseado"],
                    experiencia_ciencia=values["experiencia_ciencia"],
                    experiencia_arte=values["experiencia_arte"],
                    interes_desarrollo_comunitario=values["interes_comunitario"],
                    razones_interes=values["razones_interes"],
                    profesion_interes=values["profesion_interes"],
                    interes_incorporacion=values["interes_incorporacion"],
                    codigo_postal=values["codigo_postal"],
                    estado=values["estado"],
                    colonia=values["colonia"],
                    municipio=values["municipio"],
                    localidad=values["localidad"],
                    calle=values["calle"],
                    numero_exterior=values["numero_exterior"],
                    numero_interior=values["numero_interior"],
                    certificado=certificado_url,
                    identificacion=identificacion_url,
                    estado_cuenta=estado_cuenta_url,
                )

                # # Crear un registro en el modelo LEC
                # lec = LEC.objects.create(
                #     nombre=values["nombres"],
                #     apellido_paterno=values["apellido_paterno"],
                #     apellido_materno=values["apellido_materno"],
                #     estado=values["estado"],
                #     municipio=values["municipio"],
                #     localidad=values["localidad"],
                #     centro_asignado=models.ForeignKey('CentroComunitario', on_delete=models.SET_NULL, null=True, blank=True),
                # )

                # Inscribir candidato a convocatoria
                convocatoria=Convocatoria.objects.get(
                    id=values["convocatoria"])
                    
                fecha_inscripcion=timezone.now().date()
                inscripcion=Inscripciones.objects.create(
                    usuario=detallesUsuario,
                    convocatoria=convocatoria,
                    fecha_inscripcion=fecha_inscripcion
                )
                
                # Enviar correo de confirmación
                token = authenticate()
                contenido = mensaje_registro_exitoso(values["nombres"])
                send_mail(destination=values["correo"],subject='¡Registro SIGEFE exitoso!',body=contenido, token=token)
                

        return Response({"message": "Tu registro ha sido exitoso"})

@permission_classes([IsAuthenticated])
class DetallesUsuarioListView(APIView):
    def get(self, request):
        detalles_usuarios=DetallesUsuario.objects.filter(estado_aceptacion="Pendiente")
        serializer=DetallesUsuarioSerializer(detalles_usuarios, many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])    
class SaS_URL(APIView):
    def post(self, request):
        data = json.loads(request.body)
        url = data.get('url')
        if url == "/":
            return Response({"url_sas": url}, status=200)
        params = url.split('/')
        url_sas = generate_sas_url(blob_name=params[4], container_name=params[3], blob_url=url) 
        return Response({"url_sas": url_sas}, status=200) 

@permission_classes([IsAuthenticated])
class CambiarEstadoAceptacion(APIView):
    def patch(self, request, pk, action=None):
        try:
            # Obtener el objeto DetallesUsuario
            detalles_usuario=DetallesUsuario.objects.get(pk=pk)
        except DetallesUsuario.DoesNotExist:
            return Response({"error": "DetallesUsuario no encontrado."})

        # Determinar el estado basado en la acción
        if action == "aceptar":
            detalles_usuario.estado_aceptacion="Aceptado"
        elif action == "rechazar":
            detalles_usuario.estado_aceptacion="Rechazado"
        else:
            return Response({"error": "Acción no valida."})

        # Guardar el cambio
        detalles_usuario.save()
        return Response(
            {"mensaje": "OK"}, status=200,
        )
        
@permission_classes([IsAuthenticated])
class ConsultarConvocatoriasInscripcion(APIView):
    def get(self, request):
        convocatorias = Convocatoria.objects.filter(fecha_entrega_resultados__gte=timezone.now().date())
        convocatorias_incompletas = []
        for convocatoria in convocatorias:
            inscripciones = Inscripciones.objects.filter(convocatoria=convocatoria)
            if len(inscripciones) < convocatoria.max_participantes:
                convocatorias_incompletas.append(convocatoria)        
        serializer = ConvocatoriaSerializer(convocatorias_incompletas, many=True)
        return Response(serializer.data)            
        
@permission_classes([IsAuthenticated])
class ConsultarCandidatosInscritos(APIView):
    def post(self, request):
        # Obtener el id de la convocatoria
        data = json.loads(request.body)
        id_convocatoria = data.get('id_convocatoria')
        # Obtener los candidatos inscritos en la convocatoria que el estado_aceptacion sea "Aceptado" y estado_aprobacion sea "Pendiente"
        inscripciones = Inscripciones.objects.filter(convocatoria=id_convocatoria, usuario__estado_aceptacion="Aceptado", estado_aprobacion="Pendiente")
        
        candidatos = [{"usuario": inscripcion.usuario, "inscripcion_id": inscripcion.id} for inscripcion in inscripciones]
        serializer = DetallesUsuarioSerializer([candidato["usuario"] for candidato in candidatos], many=True)
        for i, candidato in enumerate(candidatos):
            candidato["usuario"] = serializer.data[i]
        return Response({"candidatos": candidatos}, status=200)
    
@permission_classes([IsAuthenticated])
class CambiarAceptacion(APIView):
    def patch(self, request, pk, action=None):
        inscripcion = Inscripciones.objects.get(pk=pk)
        """ try:
            # Obtener el objeto de Inscripciones con el usuario_id que viene como pk 
            inscripcion = Inscripciones.objects.get(pk=pk)
        except Inscripciones.DoesNotExist:
            return Response({"error": "Inscripcion no encontrado."}, status=status.HTTP_404_NOT_FOUND)
 """
        print(pk)
        #print(inscripcion)

        detalles_usuario = inscripcion.usuario
        values = {
            "nombres": detalles_usuario.nombres,
            "correo": detalles_usuario.usuario.email,
            "lugar_convocatoria": inscripcion.convocatoria.lugar_convocatoria
        }
        # Determinar el estado basado en la acción
        if action == "aceptar":
            inscripcion.estado_aprobacion = "Aceptado"  # Asegúrate de actualizar el estado de aprobación
            # Crear o actualizar el objeto LEC
            lec, created = LEC.objects.get_or_create(
                email=detalles_usuario.usuario.email,
                defaults={
                    "nombre": detalles_usuario.nombres,
                    "apellido_paterno": detalles_usuario.apellido_paterno,
                    "apellido_materno": detalles_usuario.apellido_materno,
                    "estado": detalles_usuario.estado,
                    "municipio": detalles_usuario.municipio,
                    "localidad": detalles_usuario.localidad,
                    "id_usuario": detalles_usuario.id
                }
            )
            # Actualizar datos en caso de que ya exista
            lec.nombre = detalles_usuario.nombres
            lec.apellido_paterno = detalles_usuario.apellido_paterno
            lec.apellido_materno = detalles_usuario.apellido_materno
            lec.estado = detalles_usuario.estado
            lec.municipio = detalles_usuario.municipio
            lec.localidad = detalles_usuario.localidad
            lec.estado_aceptacion = "Aceptado"
            lec.detalles_usuario = detalles_usuario  # Asegurarse de asignar detalles_usuario
            lec.save()
            
            # Enviar correo de aceptación
            token = authenticate()
            contenido = mensaje_aceptacion(values["nombres"], values["lugar_convocatoria"])
            send_mail(destination=values["correo"], subject='Aceptacion a la CONAFE como LEC', body=contenido, token=token)
            
        elif action == "rechazar":
            inscripcion.estado_aprobacion = "Rechazado"
            token = authenticate()
            contenido = mensaje_rechazo(values["nombres"], values["lugar_convocatoria"])
            send_mail(destination=values["correo"], subject='Rechazo a la CONAFE como LEC', body=contenido, token=token)
        else:
            return Response({"error": "Acción no valida."})

        # Guardar el cambio
        inscripcion.save()
        return Response({"mensaje": "OK"}, status=200)