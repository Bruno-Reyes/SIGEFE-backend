# python manage.py shell < utils/crear_convocatorias.py

from ALC100_captacion.models.models import Convocatoria
import random
from utils.estados import estados

def crear_convocatorias():
    # Crear 32 registros de convocatorias para el año 2025 una por cada estado de la república mexicana y la CDMX, con el numero de participantes entre 50 y 250

    print("Creando convocatorias...")

    for estado in estados:
        # Crea un registro de Convocatoria  para el año 2025 con el lugar de la convocatoria (variable del for "estado"), fecha límite de registro, fecha de entrega de resultados y un número aleatorio de participantes entre 50 y 250
        Convocatoria.objects.create(
            lugar_convocatoria=estado,
            fecha_limite_registro='2025-01-01',
            fecha_entrega_resultados='2025-01-15',
            max_participantes=random.randint(5, 50)
        )
        print(f"Convocatoria creada para {estado}")

    for estado in estados:
        # Crea un registro de Convocatoria  para el año 2024 con el lugar de la convocatoria (variable del for "estado"), fecha límite de registro, fecha de entrega de resultados y un número aleatorio de participantes entre 50 y 250
        Convocatoria.objects.create(
            lugar_convocatoria=estado,
            fecha_limite_registro='2024-06-01',
            fecha_entrega_resultados='2025-01-15',
            max_participantes=random.randint(50, 250)
        )
        print(f"Convocatoria creada para {estado}")
    
    print("Convocatorias creadas exitosamente")