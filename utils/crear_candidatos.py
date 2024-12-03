# python manage,py shell < utils/crear_candidatos.py
from ALC100_captacion.models.models import DetallesUsuario, Inscripciones, Convocatoria
from ALC000_sistema_base.models.models import Usuario, TipoUsuario
from django.utils import timezone
from utils.helpers import CREAR_DETALLES_USUARIO, generar_data_users 
from random import sample

# Cre una funcion que cree un usuario con datos sinteticos (email, password)
def crear_candidatos(n : int):
    # Obtener las convocatorias activas
    convocatorias = Convocatoria.objects.filter(fecha_limite_registro__gte=timezone.now().date())
    # Extraer los ids de las convocatorias activas y guardar en una lista
    ids_convocatorias = [convocatoria.id for convocatoria in convocatorias]
        
    #Genera datos sinteticos
    generar_data_users('utils/data_users.txt', n)
    # Lee el archivo de datos sinteticos
    with open("utils/data_users.txt", "r") as f:
        datos_sinteticos = f.readlines()
        for usuario in datos_sinteticos:
            email, password = usuario.split("-")
            # Crea un usuario con datos sinteticos
            usuario = Usuario.objects.create_user(
                email=email,
                password=password,
                tipo_usuario=TipoUsuario.ASPIRANTE_LEC,
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
                talla_playera = detalles["talla_playera"],
                talla_pantalon = detalles["talla_pantalon"],
                talla_calzado = detalles["talla_calzado"],
                peso = detalles["peso"],
                estatura = detalles["estatura"],
                banco = detalles["banco"],
                clabe = detalles["clabe"],
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
            
            # Seleccionar el id de una convocatoria activa aleatoriamente
            id = sample(ids_convocatorias, 1)[0]
            # Obtener la convocatoria seleccionada
            convocatoria = Convocatoria.objects.get(id=id)
            # Crear una inscripcion con la convocatoria seleccionada
            inscripcion = Inscripciones.objects.create(
                convocatoria = convocatoria,
                usuario = detallesUsuario
            )

        f.close()

        # Imprimir todas las inscripcones
        inscripciones = Inscripciones.objects.all()
        for inscripcion in inscripciones:
            print(inscripcion)

        # Imprimir mensaje de exito
        print("Candidatos creados correctamente")
    