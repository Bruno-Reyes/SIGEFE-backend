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

    def validate_dates_and_overlap(self, lugar, fecha_limite, fecha_resultados):
        fecha_actual = timezone.now().date()
        
        # Validar que las fechas no sean anteriores a la actual
        if fecha_limite < fecha_actual:
            return False, "La fecha límite de registro no puede ser anterior a la fecha actual"
        
        if fecha_resultados < fecha_actual:
            return False, "La fecha de entrega de resultados no puede ser anterior a la fecha actual"
            
        if fecha_resultados < fecha_limite:
            return False, "La fecha de resultados no puede ser anterior a la fecha límite de registro"
        
        # Validar traslape de convocatorias
        convocatorias_existentes = Convocatoria.objects.filter(
            lugar_convocatoria=lugar,
            fecha_limite_registro__gte=fecha_actual
        )
        
        if convocatorias_existentes.exists():
            return False, "Ya existe una convocatoria activa para este lugar"
            
        return True, ""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lugar = serializer.validated_data['lugar_convocatoria']
            fecha_limite = serializer.validated_data['fecha_limite_registro']
            fecha_resultados = serializer.validated_data['fecha_entrega_resultados']
            
            is_valid, error_message = self.validate_dates_and_overlap(lugar, fecha_limite, fecha_resultados)
            if not is_valid:
                return Response(
                    {"error": error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return super().create(request, *args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            lugar = serializer.validated_data.get('lugar_convocatoria', instance.lugar_convocatoria)
            fecha_limite = serializer.validated_data.get('fecha_limite_registro', instance.fecha_limite_registro)
            fecha_resultados = serializer.validated_data.get('fecha_entrega_resultados', instance.fecha_entrega_resultados)
            
            # Solo validar si se están actualizando las fechas o el lugar
            if 'lugar_convocatoria' in serializer.validated_data or \
               'fecha_limite_registro' in serializer.validated_data or \
               'fecha_entrega_resultados' in serializer.validated_data:
                
                is_valid, error_message = self.validate_dates_and_overlap(lugar, fecha_limite, fecha_resultados)
                if not is_valid:
                    return Response(
                        {"error": error_message},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            return super().update(request, *args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                email_error = False
                try:
                    token = authenticate()
                    contenido = mensaje_registro_exitoso(values["nombres"])
                    send_mail(destination=values["correo"],subject='¡Registro SIGEFE exitoso!',body=contenido, token=token)
                except Exception as e:
                    print(f"Error al enviar el correo: {str(e)}")
                    email_error = True

        return Response({"message": "Tu registro ha sido exitoso", "email_error": email_error})

@permission_classes([IsAuthenticated])
class DetallesUsuarioListView(APIView):
    def get(self, request):
        detalles_usuarios=DetallesUsuario.objects.filter(estado_aceptacion="Pendiente")
        serializer=DetallesUsuarioSerializer(detalles_usuarios, many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class DetallesAllUsers(APIView):
    def get(self, request):
        detalles_usuarios=DetallesUsuario.objects.filter(estado_aceptacion="Aceptado")
        serializer=DetallesUsuarioSerializer(detalles_usuarios, many=True)
        return Response(serializer.data)
    
class DetallesUsuarioPorID(APIView):
    """
    Endpoint para obtener los detalles de un usuario específico por su `usuario_id`.
    GET: /api/detalles-usuario/<int:usuario_id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id):
        try:
            # Filtrar por `usuario_id` y estado de aceptación
            detalle_usuario = DetallesUsuario.objects.get(usuario_id=usuario_id, estado_aceptacion="Aceptado")
        except DetallesUsuario.DoesNotExist:
            return Response({"error": "No se encontró ningún usuario con el ID proporcionado."}, status=404)

        # Serializar los datos
        serializer = DetallesUsuarioSerializer(detalle_usuario)
        return Response(serializer.data, status=200)
    
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
            detalles_usuario = DetallesUsuario.objects.get(pk=pk)
        except DetallesUsuario.DoesNotExist:
            return Response({"error": "DetallesUsuario no encontrado."})

        # Determinar el estado basado en la acción
        if action == "aceptar":
            detalles_usuario.estado_aceptacion = "Aceptado"
        elif action == "rechazar":
            detalles_usuario.estado_aceptacion = "Rechazado"
        else:
            return Response({"error": "Acción no valida."})

        # Guardar el cambio
        detalles_usuario.save()

        # Enviar correo de notificación
        email_error = False
        try:
            token = authenticate()
            if action == "aceptar":
                contenido = mensaje_aceptacion(detalles_usuario.nombres, detalles_usuario.usuario.email)
                send_mail(destination=detalles_usuario.usuario.email, subject='Aceptación de la CONAFE como LEC', body=contenido, token=token)
            elif action == "rechazar":
                contenido = mensaje_rechazo(detalles_usuario.nombres, detalles_usuario.usuario.email)
                send_mail(destination=detalles_usuario.usuario.email, subject='Rechazo de la CONAFE como LEC', body=contenido, token=token)
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
            email_error = True

        return Response({
            "mensaje": "OK",
            "email_error": email_error
        }, status=200)

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
            
            email_error = False
        try:
            # Enviar correo de aceptación o rechazo
            token = authenticate()
            if action == "aceptar":
                contenido = mensaje_aceptacion(values["nombres"], values["lugar_convocatoria"])
                send_mail(destination=values["correo"], subject='Aceptacion de la CONAFE como LEC', body=contenido, token=token)
            elif action == "rechazar":
                inscripcion.estado_aprobacion = "Rechazado"
                contenido = mensaje_rechazo(values["nombres"], values["lugar_convocatoria"])
                send_mail(destination=values["correo"], subject='Rechazo de la CONAFE como LEC', body=contenido, token=token)
            else:
                return Response({"error": "Acción no valida."})
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
            email_error = True
    
        # Guardar el cambio
        inscripcion.save()
        return Response({
                "message": f"LEC Validado exitosamente.",
                "email_error": email_error
            }, status=status.HTTP_200_OK)