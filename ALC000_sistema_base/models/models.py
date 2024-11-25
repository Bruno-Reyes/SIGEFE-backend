from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y devuelve un usuario con un email y contraseña.
        """
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Establecer la contraseña de manera segura
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y devuelve un superusuario con un email y contraseña.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class TipoUsuario(models.TextChoices):
    ASPIRANTE_LEC = "aspirante_lec", "Aspirante a Líder para la Educación Comunitaria"
    COORD_NAC_RRHH = "coord_nac_rrhh", "Coordinador Nacional de Recursos Humanos"
    LIDER_LEC = "lider_lec", "Líder para la Educación Comunitaria"
    COORD_ACADEMICO = "coord_academico", "Coordinador Académico"
    AUX_OPERACION = "aux_operacion", "Auxiliar de Operación"
    COORD_NAC_LOGISTICA = "coord_nac_logistica", "Coordinador Nacional de Apoyo y Logística"
    COORD_OPERATIVO = "coord_operativo", "Coordinador Operativo"

class Usuario(AbstractUser):
    username = None  # Eliminar el campo username
    email = models.EmailField(unique=True)  # Usar email como identificador único
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ASPIRANTE_LEC,
    )

    # Usar el UserManager personalizado
    objects = UsuarioManager()

    def __str__(self):
        return f"{self.email} ({self.get_tipo_usuario_display()})"

    # Opcional: Hacer que el email sea usado para autenticación
    USERNAME_FIELD = 'email'  # Esto indica que se usará el email para la autenticación
    REQUIRED_FIELDS = []  # El campo 'email' será requerido para la creación de un superusuario, pero 'username' ya no será necesario
