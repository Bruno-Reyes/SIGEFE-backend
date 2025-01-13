from django.db import models
from ALC000_sistema_base.models.models import Usuario

# Tabla PagoApoyo
class PagoApoyo(models.Model):
    CONCEPTOS = [
        ('Beca', 'Beca'),
        ('Seguimiento', 'Seguimiento'),
        ('Continuacion', 'Continuacion'),
        ('Apoyo Mensual de Servicio', 'Apoyo Mensual de Servicio'),
        ('Beca de Continuidad 30 Meses', 'Beca de Continuidad 30 Meses'),
        ('Beca de Continuidad 60 Meses', 'Beca de Continuidad 60 Meses'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
    ]

    CONFIRMACIONES = [
        ('recibido', 'Recibido'),
        ('error', 'Error'),
        ('no_recibido', 'No Recibido'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pagos")
    concepto = models.CharField(max_length=50, choices=CONCEPTOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    registrado_por = models.EmailField()
    confirmacion_lec = models.CharField(
        max_length=20,
        choices=CONFIRMACIONES,
        null=True,
        blank=True
    )  # Nuevo campo

    def __str__(self):
        return f"{self.usuario.email} - {self.concepto} - {self.monto} - {self.estatus} - {self.confirmacion_lec}"


# Tabla ALC004TiposBecas
class ALC004TiposBecas(models.Model):
    tipo = models.CharField(max_length=50, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"


# Nueva tabla ALC401LecBecas
class ALC401LecBecas(models.Model):
    tipo_beca = models.ForeignKey(ALC004TiposBecas, on_delete=models.CASCADE, related_name="asignaciones")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="becas")
    estatus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.email} - {self.tipo_beca.tipo} - Estatus: {self.estatus}"
