import random
from utils.estados import estados

""""Función para generar un email de prueba aleatorio y único guardando los resultdos en un archivo.txt"""

def generar_email_prueba():
    nombres = ["usuario", "prueba", "test", "demo"]
    dominios = ["example.com", "test.com", "demo.com"]
    numero = random.randint(1, 1000)
    numero2 = str(numero).zfill(3)  # Rellenar con ceros a la izquierda
    numero3 = random.randint(1, 1000)
    nombre = random.choice(nombres)
    dominio = random.choice(dominios)
    email = f"{nombre}{numero}{numero2}{numero3}@{dominio}"
    return email

# Función para generar una contraseña de prueba aleatoria
def generar_password_prueba():
    longitud = random.randint(5,8)
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
    password = "".join(random.choices(caracteres, k=longitud))
    return password

def generar_data_users(path_file, n_users):
    for _ in range(n_users):
        # Generar un email de prueba
        email = generar_email_prueba()
        # Generar una contraseña de prueba
        password = generar_password_prueba()
        # Guardar el email y contraseña en un archivo
        with open(path_file, "a") as f:
            f.write(f"{email}-{password}\n")
        f.close()
    
    with open(path_file, 'r') as file:
        lineas = file.readlines()

    correos = set()
    duplicados = []

    for linea in lineas:
        email, _ = linea.split('-')
        if email in correos:
            duplicados.append(email)
        else:
            correos.add(email)

    if duplicados:
        print("Correos duplicados encontrados:")
        for correo in duplicados:
            print(correo)
    else:
        print("No se encontraron correos duplicados.")

# Ejemplo de uso
# generar_data_users('utils/data_users.txt', 5000)

# Genera una funcion para crear un CURP aleasorio
def generar_curp():
    vocales = "AEIOU"
    consonantes = "BCDFGHJKLMNPQRSTVWXYZ"
    numeros = "1234567890"
    curp = ""
    curp += random.choice(consonantes)  # Primer consonante del apellido paterno
    curp += random.choice(vocales)  # Primera vocal del apellido paterno
    curp += random.choice(consonantes)  # Primera consonante del apellido materno
    curp += random.choice(consonantes)  # Primera consonante del primer nombre
    curp += random.choice(numeros)  # Último dígito del año de nacimiento
    curp += random.choice(numeros)  # Penúltimo dígito del año de nacimiento
    curp += random.choice(numeros)  # Tercer dígito del año de nacimiento
    curp += random.choice(numeros)  # Cuarto dígito del año de nacimiento
    curp += random.choice(consonantes)  # Letra del mes de nacimiento
    curp += random.choice(numeros)  # Día de nacimiento
    curp += random.choice(numeros)  # Segundo dígito del día de nacimiento
    curp += random.choice(vocales)  # Letra del estado de nacimiento
    curp += random.choice(consonantes)  # Primer consonante del apellido paterno
    curp += random.choice(consonantes)  # Primera consonante del apellido materno
    curp += random.choice(consonantes)  # Primera consonante del primer nombre
    curp += random.choice(numeros)  # Dígito verificador
    return curp

# Genera una función para crear un nombre aleatorio
def generar_nombre():
    nombres = ["Juan", "Pedro", "María", "José", "Ana", "Luis", "Carlos", "Laura", "Rosa", "Miguel", "Sofía", "Fernando", "Diana", "Eduardo", "Dulce", "Roberto", "Verónica", "Ricardo", "Patricia", "Jorge", "Silvia", "Raúl", "Carmen", "Daniel", "Gabriela", "Alejandro", "Leticia", "Héctor", "Elena", "Oscar", "Adriana", "Francisco", "Isabel", "Javier", "Mónica", "Armando", "Norma", "Alberto", "Teresa", "Guadalupe", "Antonio", "Rosa", "Manuel", "Beatriz", "Rafael", "Claudia", "Arturo", "Nancy", "José Luis", "Martha", "Salvador", "Gloria", "Rubén", "Lorena", "Fernando", "Cecilia", "Ángel", "Yolanda", "Roberto", "Dora", "Ernesto", "Lilia", "Humberto", "Marisol", "Mauricio", "Rosa María", "Erick", "Irma", "Gerardo", "Maribel"]
    nombre = random.choice(nombres)
    return nombre

# Genera una función para crear un apellido aleatorio
def generar_apellido():
    apellidos = ["Hernández", "García", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Reyes", "Morales", "Jiménez", "Ortiz", "Silva", "Rojas", "Mendoza", "Vázquez", "Cruz", "Ruiz", "Álvarez", "Juárez", "Carrillo", "Medina", "León", "Herrera", "Aguilar", "Cortés", "Aguirre", "Guzmán", "Santos", "Fernández", "Castillo", "Valenzuela", "Campos", "Vega", "Vargas", "Castañeda", "Cervantes", "Salazar", "Pacheco", "Sosa", "Rosas", "Lara", "Cabrera", "Villanueva", "Escobar", "Bautista", "Villarreal", "Valencia", "Mata", "Gallardo", "Esparza", "Cisneros", "Lugo", "Montes", "Valdés", "Navarro", "Zamora", "Cuevas", "Cárdenas", "Aguayo", "Villalobos", "Guzmán", "Santos", "Fernández", "Castillo", "Valenzuela", "Campos", "Vega", "Vargas", "Castañeda", "Cervantes", "Salazar", "Pacheco", "Sosa", "Rosas", "Lara", "Cabrera", "Villanueva", "Escobar", "Bautista", "Villarreal", "Valencia", "Mata", "Gallardo", "Esparza", "Cisneros", "Lugo", "Montes", "Valdés", "Navarro", "Zamora", "Cuevas", "Cárdenas", "Aguayo", "Villalobos"]
    apellido = random.choice(apellidos)
    return apellido

# Genera una función para crear una fecha de nacimiento aleatoria
def generar_fecha_nacimiento():
    año = random.randint(1960, 2003)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    return f"{año}-{mes:02d}-{dia:02d}"

def generar_genero():
    generos = ["M", "F", "O"]
    genero = random.choice(generos)
    return genero

def generar_nacionalidad():
    nacionalidades = ["Mexicana", "Estadounidense", "Canadiense", "Española", "Francesa", "Alemana", "Italiana", "Argentina", "Brasileña", "Colombiana", "Chilena", "Peruana", "Ecuatoriana", "Venezolana", "Cubana", "Boliviana", "Paraguaya", "Uruguaya", "Panameña", "Costarricense", "Salvadoreña", "Guatemalteca", "Hondureña", "Nicaragüense", "Puertorriqueña", "Dominicana", "Haitiana", "Jamaicana", "Trinitense", "Barbadense", "Granadina", "Luciana", "Antiguana", "Barbudense", "Sanvicentino", "Dominiqués", "Santalucense", "Sanmartinense", "Sancristobaleño", "Nevisiano", "Beliceño", "Guayanés", "Surinamés", "Guyanés", "Figueroense", "Brasileño", "Colombiano", "Ecuatoriano", "Venezolano", "Peruano", "Chileno", "Boliviano", "Paraguayo", "Uruguayo", "Argentino", "Cubano", "Costarricense", "Salvadoreño", "Guatemalteco", "Hondureño", "Nicaragüense", "Panameño", "Puertorriqueño", "Dominicano", "Haitiano", "Jamaicano", "Trinitense", "Barbadense", "Granadino", "Luciano", "Antiguano", "Barbudense", "Sanvicentino", "Dominiqués", "Santalucense", "Sanmartinense", "Sancristobaleño", "Nevisiano", "Beliceño", "Guayanés", "Surinamés", "Guyanés", "Figueroense"]
    nacionalidad = random.choice(nacionalidades)
    return nacionalidad

def generar_talla():
    tallas = ["XS", "S", "M", "L", "XL", "XXL"]
    talla = random.choice(tallas)
    return talla

# Generrar talla de calzado entre 22 y 35
def generar_talla_calzado():
    talla = random.randint(22, 35)
    return talla

# Generar peso entre 40 y 120 kg
def generar_peso():
    peso = round(random.uniform(40, 120), 2)
    return peso

# Generar estatura entre 1.50 y 2.00 m
def generar_estatura():
    estatura = round(random.uniform(1.50, 2.00))
    return estatura

def generar_banco():
    bancos = ["BBVA", "Banamex", "Santander", "HSBC", "Banorte", "Scotiabank", "Inbursa", "Banco Azteca", "BanCoppel", "Banco del Bajío"]
    banco = random.choice(bancos)
    return banco

def generar_nivel_estudios():
    niveles = ["Primaria", "Secundaria", "Preparatoria", "Licenciatura"]
    nivel = random.choice(niveles)
    return nivel

def generar_experiencia_ciencia():
    experiencias = ["Biología", "Física", "Química", "Otro", "Ninguna"]
    experiencia = random.choice(experiencias)
    return experiencia

def generar_experiencia_arte():
    experiencias = ["Música", "Teatro", "Artes Plásticas", "Literatura", "Ninguna"]
    experiencia = random.choice(experiencias)
    return experiencia

def generar_interes_desarrollo_comunitario():
    interes = random.choice([True, False])
    return interes

def generar_razones_interes():
    razones = ["Razón 1", "Razón 2", "Razón 3", "Razón 4", "Razón 5"]
    razon = random.choice(razones)
    return razon

def generar_profesion_interes():
    profesiones = ["Profesión 1", "Profesión 2", "Profesión 3", "Profesión 4", "Profesión 5"]
    profesion = random.choice(profesiones)
    return profesion

def generar_interes_incorporacion():
    intereses = ["Interés 1", "Interés 2", "Interés 3", "Interés 4", "Interés 5"]
    interes = random.choice(intereses)
    return interes

def generar_codigo_estado_postal():
    # Diccionario con rangos aproximados de códigos postales por estado
    rangos_estados = {
        "Aguascalientes": (20000, 20999),
        "Baja California": (21000, 22999),
        "Baja California Sur": (23000, 23999),
        "Campeche": (24000, 24999),
        "Coahuila": (25000, 27999),
        "Colima": (28000, 28999),
        "Chiapas": (29000, 30999),
        "Chihuahua": (31000, 33999),
        "Ciudad de México": (1000, 19999),  # Nota: ajustar rango por ceros a la izquierda
        "Durango": (34000, 35999),
        "Guanajuato": (36000, 38999),
        "Guerrero": (39000, 41999),
        "Hidalgo": (42000, 43999),
        "Jalisco": (44000, 49999),
        "Estado de México": (50000, 57999),
        "Michoacán": (58000, 61999),
        "Morelos": (62000, 62999),
        "Nayarit": (63000, 63999),
        "Nuevo León": (64000, 67999),
        "Oaxaca": (68000, 71999),
        "Puebla": (72000, 75999),
        "Querétaro": (76000, 76999),
        "Quintana Roo": (77000, 77999),
        "San Luis Potosí": (78000, 79999),
        "Sinaloa": (80000, 82999),
        "Sonora": (83000, 85999),
        "Tabasco": (86000, 86999),
        "Tamaulipas": (87000, 89999),
        "Tlaxcala": (90000, 90999),
        "Veracruz": (91000, 96999),
        "Yucatán": (97000, 97999),
        "Zacatecas": (98000, 99999),
    }

    # Seleccionar un estado al azar
    estado = random.choice(list(rangos_estados.keys()))

    # Generar un código postal aleatorio dentro del rango del estado
    rango = rangos_estados[estado]
    codigo_postal = random.randint(rango[0], rango[1])

    return estado, codigo_postal

def generar_colonia():
    colonias = ["Centro", "San Miguel", "San Pedro", "San Juan", "Santa María", "San Antonio", "San José", "La Paz", "La Esperanza", "La Libertad", "La Unión", "La Fe", "La Luz", "La Gloria", "La Soledad", "La Cruz", "La Palma", "La Loma", "La Cañada", "La Montaña", "La Sierra", "La Huerta", "La Rinconada", "La Joya", "La Fortuna", "La Perla", "La Isla", "La Playa", "La Marina", "La Estrella", "La Colina", "La Cumbre", "La Cascada"]
    return random.choice(colonias)

def generar_municipio():
    municipios = ["Aguascalientes", "Asientos", "Calvillo", "Cosío", "El Llano", "Jesús María", "Pabellón de Arteaga", "Rincón de Romos", "San José de Gracia", "Tepezalá", "Ensenada"]
    return random.choice(municipios)

def generar_localidad():
    localidades = ["Aguascalientes", "Jesús María", "Rincón de Romos", "San José de Gracia", "Pabellón de Arteaga", "Calvillo", "Cosío", "Tepezalá", "El Llano", "Asientos"]
    return random.choice(localidades)

def generar_calle():
    calles = ["Hidalgo", "Juárez", "Madero", "Revolución", "Zaragoza", "Morelos", "Carranza", "Gómez Farías", "Benito Juárez", "García", "Gutiérrez", "González", "Martínez", "Hernández", "López", "Díaz", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Reyes", "Morales", "Jiménez", "Ortiz", "Silva", "Rojas", "Mendoza", "Vázquez", "Cruz", "Ruiz", "Álvarez", "Juárez", "Carrillo", "Medina", "León", "Herrera", "Aguilar", "Cortés", "Aguirre", "Guzmán", "Santos"]
    return random.choice(calles)

def generar_numero_exterior():
    numero = random.randint(1, 1000)
    return numero

def generar_numero_interior():
    numero = random.randint(1, 100)
    return numero

def generar_estado_deseado():
    return random.choice(estados)

def CREAR_DETALLES_USUARIO():
    detalles = {}
    detalles["curp"] = generar_curp()
    detalles["nombres"] = generar_nombre()
    detalles["apellido_paterno"] = generar_apellido()
    detalles["apellido_materno"] = generar_apellido()
    detalles["fecha_nacimiento"] = generar_fecha_nacimiento()
    detalles["genero"] = generar_genero()
    detalles["nacionalidad"] = generar_nacionalidad()
    detalles["talla_playera"] = generar_talla()
    detalles["talla_pantalon"] = generar_talla()
    detalles["talla_calzado"] = generar_talla_calzado()
    detalles["peso"] = generar_peso()
    detalles["estatura"] = generar_estatura()
    detalles["banco"] = generar_banco()
    detalles["nivel_estudios"] = generar_nivel_estudios()
    detalles["nivel_estudios_deseado"] = detalles["nivel_estudios"]
    detalles["experiencia_ciencia"] = generar_experiencia_ciencia()
    detalles["experiencia_arte"] = generar_experiencia_arte()
    detalles["interes_desarrollo_comunitario"] = generar_interes_desarrollo_comunitario()
    detalles["razones_interes"] = generar_razones_interes()
    detalles["profesion_interes"] = generar_profesion_interes()
    detalles["interes_incorporacion"] = generar_interes_incorporacion()
    detalles["estado"],detalles["codigo_postal"]  = generar_codigo_estado_postal()
    detalles["colonia"] = generar_colonia()
    detalles["municipio"] = generar_municipio()
    detalles["localidad"] = generar_localidad()
    detalles["calle"] = generar_calle()
    detalles["numero_exterior"] = generar_numero_exterior()
    detalles["numero_interior"] = generar_numero_interior()
    detalles["estado_deseado"] = generar_estado_deseado()
    detalles["municipio_deseado"] = generar_municipio()
    detalles["certificado"] = "/"
    detalles["identificacion"] = "/"
    detalles["estado_cuenta"] = "/"

    return detalles