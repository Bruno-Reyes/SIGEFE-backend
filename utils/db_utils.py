from django.contrib.auth import get_user_model
from ALC100_captacion.models.models import DetallesUsuario, Convocatoria

def show_user(user):
    return f"Type: {type(user)} \n Correo: {user.email} \n Contraseña: {user.password} \n Tipo de usuario: {user.tipo_usuario}\n\n"

def get_users():
    User = get_user_model()

    # Obtener todos los usuarios
    usuarios = User.objects.all()

    for usuario in usuarios:
        print(show_user(usuario))

def get_convocatorias():
    total_convocatorias = Convocatoria.objects.count()
    print(f"Total de registros en Convocatoria: {total_convocatorias}")

def get_detalles_usuario():
    total_detalles = DetallesUsuario.objects.count()
    print(f"Total de registros en DetallesUsuario: {total_detalles}")
    # detalles = DetallesUsuario.objects.all()
    # for detalle in detalles:
    #     print(f"Type: {type(detalle)} \n Usuario: {detalle.usuario} \n Nombre: {detalle.nombre} \n Apellido: {detalle.apellido} \n Fecha de nacimiento: {detalle.fecha_nacimiento} \n\n")

get_detalles_usuario()