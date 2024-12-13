from ALC100_captacion.models.models import DetallesUsuario, Inscripciones, Convocatoria
from ALC000_sistema_base.models.models import Usuario, TipoUsuario


def db_info():
    # Imprime la cantidad de usuarios en la base de datos
    usuarios = Usuario.objects.all()
    print(f"Usuarios: {len(usuarios)}")

    # Imprime la cantidad de candidatos en la base de datos
    candidatos = DetallesUsuario.objects.all()
    print(f"Candidatos: {len(candidatos)}")

    # Imprime la cantidad de convocatorias en la base de datos
    convocatorias = Convocatoria.objects.all()
    print(f"Convocatorias: {len(convocatorias)}")

    # Imprime la cantidad de inscripciones en la base de datos
    inscripciones = Inscripciones.objects.all()
    print(f"Inscripciones: {len(inscripciones)}")

# db_info()

from ALC100_captacion.models.models import DetallesUsuario, Inscripciones
def mostrar_detalles_usuarios():
    usuarios = DetallesUsuario.objects.all()
    for usuario in usuarios:
        print(usuario)

mostrar_detalles_usuarios()

def mostrar_inscripciones():
    inscripciones = Inscripciones.objects.all()
    for inscripcion in inscripciones:
        print(inscripcion)

# mostrar_inscripciones()