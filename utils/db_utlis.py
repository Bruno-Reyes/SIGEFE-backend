from django.contrib.auth import get_user_model

def show_user(user):
    return f"Type: {type(user)} \n Correo: {user.email} \n Contraseña: {user.password} \n Tipo de usuario: {user.tipo_usuario}\n\n"

User = get_user_model()

# Obtener todos los usuarios
usuarios = User.objects.all()

for usuario in usuarios:
    print(show_user(usuario))