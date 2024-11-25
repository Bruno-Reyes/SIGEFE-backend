# python manage,py shell < utils/crear_candidatos.py
from ALC100_captacion.models.models import DetallesUsuario
from ALC000_sistema_base.models.models import Usuario
from utils.helpers import CREAR_DETALLES_USUARIO

# Cre una funcion que cree un usuario con datos sinteticos (email, password)
def crear_candidatos():
    # Lee el archivo de datos sinteticos
    with open("utils/data_users.txt", "r") as f:
        datos_sinteticos = f.readlines()
        for usuario in datos_sinteticos:
            email, password = usuario.split("-")
            # Crea un usuario con datos sinteticos
            usuario = Usuario.objects.create_user(
                email=email,
                password=password
            )
            detalles = CREAR_DETALLES_USUARIO()

            # Crea un candidato con datos sinteticos            
            DetallesUsuario.objects.create(                
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
            
crear_candidatos()