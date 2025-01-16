import json
from ALC200_asignacion.models.models import CentroComunitario 
from ALC200_asignacion.serializers import CentroComunitarioSerializer 
from django.db import models

# Ruta del archivo JSON
ruta_archivo = '/home/bruno-rg/Documents/SIGEFE-backend/data/Escuelas_CONAFE.json'

# Abrir y leer el archivo JSON
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)
archivo.close()

# Comprobar que no haya claves de centro de trabajo repetidas
claves_repetidas = CentroComunitario.objects.values('clave_centro_trabajo').annotate(count=models.Count('clave_centro_trabajo')).filter(count__gt=1)
if claves_repetidas.exists():
    print('Existen claves de centro de trabajo repetidas:')
    for clave in claves_repetidas:
        print(f'Clave: {clave["clave_centro_trabajo"]}, Repeticiones: {clave["count"]}')
    
    #Eliminar centros de trabajo repetidos, dejando solo uno
    for clave in claves_repetidas:
        centros_repetidos = CentroComunitario.objects.filter(clave_centro_trabajo=clave['clave_centro_trabajo'])
        # Dejar solo el primer centro y eliminar los demás
        centros_repetidos.exclude(id=centros_repetidos.first().id).delete()
else:
    print('No existen claves de centro de trabajo repetidas.')    

print('Inyectando coordenadas...\n')
# Recorrer los datos del archivo JSON
for dato in datos:
    # Buscar centro de trabajo por clave
    centro = CentroComunitario.objects.get(clave_centro_trabajo=dato['Clave del centro de trabajo'])
    centro = CentroComunitarioSerializer(centro)

    # Actualizar latitud y longitud del centro
    centro.instance.latitud = dato['Ubicación de la escuela-localidad al norte del Ecuador, expresada en grados']
    centro.instance.longitud = dato['Ubicación de la escuela-localidad al Oeste del Meridiano de Greenwich, expresada en grados']
    centro.instance.save()
    
print('Coordenadas inyectadas :) \n')

# Comprobar que ningún registro de centro de trabajo tenga latitud o longitud nula
centros_con_coords_nulas = CentroComunitario.objects.filter(latitud__isnull=True) | CentroComunitario.objects.filter(longitud__isnull=True)
print('Comprobando eficacia de la inyeccion :) \n')
if centros_con_coords_nulas.exists():
    print('Existen centros de trabajo con coordenadas nulas:')
    for centro in centros_con_coords_nulas:
        print(f'Clave: {centro.clave_centro_trabajo}')
else:
    print('No existen centros de trabajo con coordenadas nulas.')