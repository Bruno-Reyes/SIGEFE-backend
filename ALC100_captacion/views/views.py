# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ALC100_captacion.models.models import Convocatoria
from ALC100_captacion.serializers import ConvocatoriaSerializer
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

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
class RegistrarCandidato(APIView):
    def post(self, request):
        # Registrar candidato
        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        print(password)

        # Crea un usuario con datos sinteticos
        usuario = Usuario.objects.create_user(
            email=email,
            password=password,
            tipo_usuario= TipoUsuario.ASPIRANTE_LEC,
        )
        detalles = CREAR_DETALLES_USUARIO()
        # Crea un candidato con datos sinteticos            
        detallesUsuario = DetallesUsuario.objects.create(                
            usuario = usuario,
            curp = detalles["curp"],
            nombres = detalles["nombres"],
            apellido_paterno = detalles["apellido_paterno"],
            apellido_materno = detalles["apellido_materno"],
            fecha_nacimiento = detalles["fecha_nacimiento"],
            genero = detalles["genero"],
            nacionalidad = detalles["nacionalidad"],
            talla_playera = detalles["talla_playera"],
            talla_pantalon = detalles["talla_pantalon"],
            talla_calzado = detalles["talla_calzado"],
            peso = detalles["peso"],
            estatura = detalles["estatura"],
            banco = detalles["banco"],
            nivel_estudios = detalles["nivel_estudios"],
            nivel_estudios_deseado = detalles["nivel_estudios_deseado"],
            experiencia_ciencia = detalles["experiencia_ciencia"],
            experiencia_arte = detalles["experiencia_arte"],
            interes_desarrollo_comunitario = detalles["interes_desarrollo_comunitario"],
            razones_interes = detalles["razones_interes"],
            profesion_interes = detalles["profesion_interes"],
            interes_incorporacion = detalles["interes_incorporacion"],
            codigo_postal = detalles["codigo_postal"],
            estado = detalles["estado"],
            colonia = detalles["colonia"],
            municipio = detalles["municipio"],
            localidad = detalles["localidad"],
            calle = detalles["calle"],
            numero_exterior = detalles["numero_exterior"],
            numero_interior = detalles["numero_interior"],
            estado_deseado = detalles["estado_deseado"],
            municipio_deseado = detalles["municipio_deseado"],
            certificado = detalles["certificado"],
            identificacion = detalles["identificacion"],
            estado_cuenta = detalles["estado_cuenta"])

        # Inscribir candidato a convocatoria
        print(DetallesUsuario)
        # Convocatoria Detalles Fecha Inscripcion
        convocatoria_id = request.data.get("convocatoria_id")
        convocatoria = Convocatoria.objects.get(id=convocatoria_id)
        fecha_inscripcion = timezone.now().date()
        print(fecha_inscripcion)
        print(convocatoria)

        inscripcion = Inscripciones.objects.create(
            usuario = detallesUsuario,
            convocatoria = convocatoria,
            fecha_inscripcion = fecha_inscripcion
        )

        return Response({"message": "Candidato registrado exitosamente"})