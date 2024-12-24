from django.db import models
from ALC000_sistema_base.models.models import Usuario

# Modelo DetallesUsuario
class DetallesUsuario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="detalles",
        blank=True,
        null=True  # Hace que esta relación sea opcional
    )
    curp = models.CharField(max_length=18)
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()

    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    genero = models.CharField(max_length=1, choices=GENERO_OPCIONES)

    TALLAS_OPCIONES = [
        ('CH', 'Chica'),
        ('M', 'Mediana'),
        ('G', 'Grande'),
        ('EG', 'Extra Grande'),
    ]

    talla_playera = models.CharField(max_length=2, choices=TALLAS_OPCIONES)
    talla_pantalon = models.CharField(max_length=2, choices=TALLAS_OPCIONES)

    
    talla_calzado = models.CharField(max_length=5)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    estatura = models.DecimalField(max_digits=5, decimal_places=2)

    AFECCIONES_OPCIONES = [
        ('Diabetes', 'Diabetes'),
        ('Hipertension', 'Hipertension'),
        ('Asma', 'Asma'),
        ('Otro', 'Otro'),
        ('Ninguna', 'Ninguna')
    ]
    afecciones = models.CharField(max_length=15, choices=AFECCIONES_OPCIONES, default='Ninguna')    

    BANCO_OPCIONES = [
        ('BBVA', 'BBVA'),
        ('Banamex', 'Banamex'),
        ('Santander', 'Santander'),
        ('HSBC', 'HSBC'),
        ('Banorte', 'Banorte'),
        ('Scotiabank', 'Scotiabank'),
        ('Inbursa', 'Inbursa'),
        ('Banco Azteca', 'Banco Azteca'),
        ('BanCoppel', 'BanCoppel'),
        ('Banco del Bajío', 'Banco del Bajío'),
        ('Otro', 'Otro'),
    ]
    banco = models.CharField(max_length=50, choices=BANCO_OPCIONES)
    clabe = models.CharField(max_length=18, null=True, blank=True)

    NIVEL_ESTUDIOS_OPCIONES = [
        ('Preescolar', 'Preescolar'),
        ('Primaria', 'Primaria'),
        ('Secundaria', 'Secundaria'),
        ('Preparatoria', 'Preparatoria'),
        ('Licenciatura', 'Licenciatura'),
        ('Maestría', 'Maestría'),
        ('Doctorado', 'Doctorado'),
    ]
    nivel_estudios = models.CharField(max_length=50, choices=NIVEL_ESTUDIOS_OPCIONES)
    nivel_estudios_deseado = models.CharField(max_length=50, choices=NIVEL_ESTUDIOS_OPCIONES)
    EXPERIENCIA_CIENCIA_OPCIONES = [
        ('Biologia', 'Biología'),
        ('Fisica', 'Física'),
        ('Quimica', 'Química'),
        ('Otro', 'Otro'),
        ('Ninguna', 'Ninguna'),
    ]
    experiencia_ciencia = models.CharField(max_length=50, choices=EXPERIENCIA_CIENCIA_OPCIONES)
    EXPERIENCIA_ARTE_OPCIONES = [
        ('Musica', 'Música'),
        ('Teatro', 'Teatro'),
        ('Artes Plasticas', 'Artes Plásticas'),
        ('Literatura', 'Literatura'),
        ('Ninguna', 'Ninguna'),
    ]
    experiencia_arte = models.CharField(max_length=50, choices=EXPERIENCIA_ARTE_OPCIONES)
    interes_desarrollo_comunitario = models.BooleanField()
    RAZONES_INTERES_OPCIONES = [
        ('Recibir apoyo económico para continuar estudios', 'Recibir apoyo económico'),
        ('Tener experiencia como líder en educación comunitaria y compartir conocimientos', 'Experiencia como líder'),
        ('No perder el año y realizar alguna actividad', 'No perder el año'),
        ('Conocer personas y trabajar con niños', 'Conocer personas'),
        ('Apoyar y participar en programas sociales', 'Apoyar en programas sociales'),
    ]
    razones_interes = models.CharField(max_length=100, choices=RAZONES_INTERES_OPCIONES)

    PROFESIONES_INTERES_OPCIONES = [
        ('Ingeniería', 'Ingeniería'),
        ('Ciencias de la Salud', 'Ciencias de la Salud'),
        ('Ciencias Sociales', 'Ciencias Sociales'),
        ('Ciencias Exactas', 'Ciencias Exactas'),
        ('Ciencias Naturales', 'Ciencias Naturales'),
        ('Artes', 'Artes'),
        ('Humanidades', 'Humanidades'),
        ('Otro', 'Otro'),
    ]
    profesion_interes = models.CharField(max_length=50, choices=PROFESIONES_INTERES_OPCIONES)
    INTERES_INCORPORACION_OPCIONES = [
        ('Prácticas profesionales', 'Prácticas profesionales'),
        ('Servicio social', 'Servicio social'),
        ('Residencia profesional', 'Residencia profesional'),
        ('Movilidad académica', 'Movilidad académica'),
        ('Participación voluntaria', 'Participación voluntaria'),
    ]
    interes_incorporacion = models.CharField(max_length=50, choices=INTERES_INCORPORACION_OPCIONES)
    codigo_postal = models.CharField(max_length=5)
    ESTADOS_OPCIONES = [
        ( 'Aguascalientes', 'Aguascalientes'),
        ( 'Baja California', 'Baja California'),
        ( 'Baja California Sur', 'Baja California Sur'),
        ( 'Campeche', 'Campeche'),
        ( 'CDMX', 'CDMX' ),
        ( 'Chiapas', 'Chiapas'),
        ( 'Chihuahua', 'Chihuahua'),
        ( 'Coahuila', 'Coahuila'),
        ( 'Colima', 'Colima'),
        ( 'Durango', 'Durango'),
        ( 'Guanajuato', 'Guanajuato'),
        ( 'Guerrero', 'Guerrero'),
        ( 'Hidalgo', 'Hidalgo'),
        ( 'Jalisco', 'Jalisco'),
        ( 'Mexico', 'México'),
        ( 'Michoacan', 'Michoacán'),
        ( 'Morelos', 'Morelos'),
        ( 'Nayarit', 'Nayarit'),
        ( 'Nuevo León', 'Nuevo León'),
        ( 'Oaxaca', 'Oaxaca'),
        ( 'Puebla', 'Puebla'),
        ( 'Querétaro', 'Querétaro'),
        ( 'Quintana Roo', 'Quintana Roo'),
        ( 'San Luis Potosí', 'San Luis Potosí'),
        ( 'Sinaloa', 'Sinaloa'),
        ( 'Sonora', 'Sonora'),
        ( 'Tabasco', 'Tabasco'),
        ( 'Tamaulipas', 'Tamaulipas'),
        ( 'Tlaxcala', 'Tlaxcala'),
        ( 'Veracruz', 'Veracruz'),
        ( 'Yucatan', 'Yucatán'),
        ( 'Zacatecas', 'Zacatecas')
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS_OPCIONES)
    colonia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50, blank=True)
    calle = models.CharField(max_length=50)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True)

    certificado = models.CharField(max_length=500, blank=True)
    identificacion = models.CharField(max_length=500, blank=True)
    estado_cuenta = models.CharField(max_length=500, blank=True)
    aprobacion = models.BooleanField(default=False)

    def __str__(self):
        # Retorna todos los datos de detalles de usuario de forma legible
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno} - {self.curp} - {self.fecha_nacimiento} - {self.genero} - {self.talla_playera} - {self.talla_pantalon} - {self.talla_calzado} - {self.peso} - {self.estatura} - {self.afecciones} - {self.banco} - {self.clabe} - {self.nivel_estudios} - {self.nivel_estudios_deseado} - {self.experiencia_ciencia} - {self.experiencia_arte} - {self.interes_desarrollo_comunitario} - {self.razones_interes} - {self.profesion_interes} - {self.interes_incorporacion} - {self.codigo_postal} - {self.estado} - {self.colonia} - {self.municipio} - {self.localidad} - {self.calle} - {self.numero_exterior} - {self.numero_interior} - {self.certificado} - {self.identificacion} - {self.estado_cuenta}, {self.aprobacion}"    

# Modelo Convocatoria
class Convocatoria(models.Model):
    lugar_convocatoria = models.CharField(max_length=50)
    fecha_limite_registro = models.DateField()
    fecha_entrega_resultados = models.DateField()
    max_participantes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} Convocatoria  de: {self.lugar_convocatoria} con {self.max_participantes} \n Fecha limite de registro: {self.fecha_limite_registro} \n Fecha de entrega de resultados: {self.fecha_entrega_resultados}" 

class Inscripciones(models.Model): 
    convocatoria = models.ForeignKey(
        Convocatoria,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    usuario = models.ForeignKey(
        DetallesUsuario,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} inscrito en {self.convocatoria.lugar_convocatoria} el {self.fecha_inscripcion}"