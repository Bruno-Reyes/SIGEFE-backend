# python manage.py shell < crear_usuarios.py

from ALC000_sistema_base.models.models import Usuario, TipoUsuario

# Crear usuario Aspirante a Líder para la Educación Comunitaria
usuario_aspirante = Usuario.objects.create_user(
    email='aspirante@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.ASPIRANTE_LEC
)

# Crear Coordinador Nacional de Recursos Humanos
usuario_coord_nac_rrhh = Usuario.objects.create_user(
    email='coord_nac_rrhh@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.COORD_NAC_RRHH
)

# Crear Coordinador Académico
usuario_coord_academico = Usuario.objects.create_user(
    email='coord_academico@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.COORD_ACADEMICO
)

# Crear Auxiliar de Operación
usuario_aux_operacion = Usuario.objects.create_user(
    email='aux_operacion@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.AUX_OPERACION
)

# Crear Coordinador Nacional de Apoyo y Logística
usuario_coord_nac_logistica = Usuario.objects.create_user(
    email='coord_nac_logistica@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.COORD_NAC_LOGISTICA
)

# Crear Coordinador Operativo
usuario_coord_operativo = Usuario.objects.create_user(
    email='coord_operativo@example.com',
    password='contraseña_segura',
    tipo_usuario=TipoUsuario.COORD_OPERATIVO
)

# Verificar que se crearon correctamente los usuarios
for usuario in Usuario.objects.all():
    print(usuario.email, usuario.tipo_usuario, usuario.password)

