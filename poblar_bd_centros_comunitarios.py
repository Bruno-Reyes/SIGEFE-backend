import mysql.connector
import json
import math
# Cargar datos del archivo .env
from dotenv import load_dotenv
import os

load_dotenv()

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USERNAME'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_NAME_DATABASE'),
    port=os.getenv('MYSQL_PORT')
)

cursor = conn.cursor()

# Leer datos del archivo JSON
with open('C:/Users/lawli/OneDrive/Documentos/GitHub/SIGEFE/SIGEFE-frontend/src/tools/Escuelas_CONAFE.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Insertar datos en la tabla CentroComunitario
query = '''
INSERT INTO ALC200_asignacion_centrocomunitario 
(clave_centro_trabajo, estado, municipio, nombre_localidad, codigo_postal, nombre_turno, nivel_educativo, domicilio, vacantes) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

def get_value(data, key, default=None):
    value = data.get(key)
    if isinstance(value, float) and math.isnan(value):
        return default
    return value

contador = 1
n_centros = len(json_data)

for data in json_data:
    values = (
            get_value(data, 'Clave del centro de trabajo'),
            get_value(data, 'Nombre de la entidad'),
            get_value(data, 'Nombre del municipio o delegación'),
            get_value(data, 'Nombre de localidad'),
            get_value(data, 'Código postal'),
            get_value(data, 'Nombre del turno'),
            get_value(data, 'Nivel educativo', 'No especificado'),  # Valor por defecto para nivel_educativo
            get_value(data, 'Domicilio'),
            get_value(data, 'Vacantes', 0)  # Valor por defecto para vacantes
        )
    cursor.execute(query, values)
    print(f"{contador}/{n_centros}")
    contador += 1
    conn.commit()

print("Datos insertados correctamente")

# Cerrar la conexión
cursor.close()
conn.close()