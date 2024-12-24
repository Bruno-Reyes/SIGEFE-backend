# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.serializers import ConvocatoriaSerializer
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from ALC100_captacion.services import subir_archivo_azure
from ALC000_sistema_base.services import enviar_email
import json

# Provisional
from ALC000_sistema_base.models.models import Usuario
from ALC100_captacion.models.models import DetallesUsuario
from ALC100_captacion.models.models import Inscripciones
from utils.helpers import CREAR_DETALLES_USUARIO
from ALC000_sistema_base.models.models import TipoUsuario


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

@permission_classes([AllowAny])  
class ObtenerActivas(APIView):
    def get(self, request):
        fecha_actual = timezone.now().date()
        convocatorias = Convocatoria.objects.filter(fecha_limite_registro__gte=fecha_actual)
        serializer = ConvocatoriaSerializer(convocatorias, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
class RegistrarCandidato(APIView):
    def post(self, request):
        # Registrar candidato
        values = json.loads(request.data.get("data") )
        # Validar un unico email desde servidor
        usuario = Usuario.objects.filter(email=values["correo"])
        if usuario:
            return Response({"detail": "El correo ya ha sido registrado"}, status=400)
        else: 
            # Extramos los archivos y los guardamos en azure
            fichero_certificado = request.data.get("files[0]")
            fichero_identificacion = request.data.get("files[1]")
            fichero_estado_cuenta = request.data.get("files[2]")

            # Subir archivos a azure
            certificado_url = subir_archivo_azure(fichero_certificado, "certificados")
            identificacion_url = subir_archivo_azure(fichero_identificacion, "identificaciones")
            estado_cuenta_url = subir_archivo_azure(fichero_estado_cuenta, "cuentas")

            if not certificado_url or not identificacion_url or not estado_cuenta_url:
                return Response({"detail": "Error al subir archivos"}, status=400)
            else:
                # Crea un usuario con datos sinteticos
                usuario = Usuario.objects.create_user(
                    email=values["correo"],
                    password=values["contrasena"],
                    tipo_usuario= TipoUsuario.ASPIRANTE_LEC,
                )
                
                # Crea un candidato con datos sinteticos            
                detallesUsuario = DetallesUsuario.objects.create(                
                    usuario = usuario,
                    curp = values["curp"],
                    nombres = values["nombres"],
                    apellido_paterno = values["apellido_paterno"],
                    apellido_materno = values["apellido_materno"],
                    fecha_nacimiento = values["fecha_nacimiento"].split("T")[0],
                    genero = values["genero"],
                    talla_playera = values["talla_playera"],
                    talla_pantalon = values["talla_pantalon"],
                    talla_calzado = values["talla_calzado"],
                    peso = values["peso"],
                    estatura = values["estatura"],
                    afecciones = values["afecciones"],
                    banco = values["banco"],
                    clabe = values["clabe"],
                    nivel_estudios = values["nivel_estudios"],
                    nivel_estudios_deseado = values["nivel_estudios_deseado"],
                    experiencia_ciencia = values["experiencia_ciencia"],
                    experiencia_arte = values["experiencia_arte"],
                    interes_desarrollo_comunitario = values["interes_comunitario"],
                    razones_interes = values["razones_interes"],
                    profesion_interes = values["profesion_interes"],
                    interes_incorporacion = values["interes_incorporacion"],
                    codigo_postal = values["codigo_postal"],
                    estado = values["estado"],
                    colonia = values["colonia"],
                    municipio = values["municipio"],
                    localidad = values["localidad"],
                    calle = values["calle"],
                    numero_exterior = values["numero_exterior"],
                    numero_interior = values["numero_interior"],
                    certificado = certificado_url,
                    identificacion = identificacion_url,
                    estado_cuenta = estado_cuenta_url)

                # Inscribir candidato a convocatoria
                
                # Convocatoria Detalles Fecha Inscripcion
                convocatoria = Convocatoria.objects.get(id=values["convocatoria"])
                fecha_inscripcion = timezone.now().date()
                inscripcion = Inscripciones.objects.create(
                    usuario = detallesUsuario,
                    convocatoria = convocatoria,
                    fecha_inscripcion = fecha_inscripcion
                )

                send_notification = enviar_email(email=values["correo"], subject="Registro exitoso", message="Felicitaciones, tu registro ha sido exitoso. Pronto recibirás noticias nuestras.") 
                

                return Response({"message": "Tu registro ha sido exitoso"})  

# Esta funcion debe enviar los pendientes de validacion usando un id de convocatoria como parametro


class ObtenerAspirantes(APIView):
    def get(self, request):
    
        # if not request.data.keys(): 
        #     # Enviamos el nombre de las convocatorias junto con el total de aspirantes
        #     fecha_actual = timezone.now().date()
        #     convocatorias = Convocatoria.objects.filter(fecha_entrega_resultados__gte=fecha_actual)
        #     # Imprimir el QuerySet de convocatorias
        #     for convo in convocatorias:
        #         print(convo)

        return Response({"OK": "Tu registro ha sido exitoso"})  

        # aspirantes = DetallesUsuario.objects.filter(aprobacion=False)
        # serializer = DetallesUsuarioSerializer(aspirantes, many=True)
        # return Response(serializer.data)