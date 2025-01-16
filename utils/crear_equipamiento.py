# Funcion para crear equipo disponible de forma sintetica para cada estado
from ALC600_logistica.models.models import EquipoDisponible, AsignacionMaterial
from ALC200_asignacion.models.models import CentroComunitario   
# Definiendo un diccionario con los equipos para crear
equipos = {
    'Papelería': ['Hojas blancas', 'Lápices', 'Bolígrafos', 'Cuadernos', 'Gomas de borrar'],
    'Utilería': ['Cinta adhesiva', 'Tijeras', 'Grapadora', 'Perforadora', 'Clips'],
    'Ropa y Calzado' : ['Camisetas', 'Pantalones', 'Zapatos', 'Calcetines', 'Chamarras'],
    'Mobiliario': ['Silla', 'Mesa', 'Estantería', 'Archivador', 'Pizarra']
}

# Obtener una lista de todos los centros comunitarios
centros = CentroComunitario.objects.all()

for categoria, lista_equipos in equipos.items():
    
    print(f'Asignando equipos de tipo {categoria}')
    for equipo in lista_equipos:
        # Crear el equipo disponible
        equipo_disponible = EquipoDisponible.objects.create(
            nombre_equipo=equipo,
            cantidad_disponible=0,
            descripcion=f'Equipo de la categoría {categoria}',
            categoria=categoria
        )
        print(f'Asignando {equipo} a todos los centros')
        # Asignar 50 unidades de este equipo a cada centro comunitario
        for centro in centros:
            AsignacionMaterial.objects.create(
                equipo=equipo_disponible,
                centro=centro,
                cantidad_asignada=50
            )