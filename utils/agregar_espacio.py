volumenes = {
    "Hojas blancas": 90160,
    "Lápices": 1803200,
    "Bolígrafos": 2704800,
    "Cuadernos": 450800000,
    "Gomas de borrar": 3606400,
    "Cinta adhesiva": 18032000,
    "Tijeras": 54096000,
    "Grapadora": 90160000,
    "Perforadora": 126224000,
    "Clips": 901600,
    "Camisetas": 2704800000,
    "Pantalones": 5409600000,
    "Zapatos": 10819200000,
    "Calcetines": 901600000,
    "Chamarras": 18032000000,
    "Silla": 360640000000,
    "Mesa": 721280000000,
    "Estantería": 1803200000000,
    "Archivador": 1442560000000,
    "Pizarra": 540960000000
}

from ALC600_logistica.models.models import EquipoDisponible

piezas = 1803200

for categorias in volumenes.keys():
    # print(categorias)
    # print(volumenes[categorias])
    equipo = EquipoDisponible.objects.get(nombre_equipo=categorias)
    # Actualizar el volumen
    equipo.volumen = round((volumenes[categorias]/piezas), 4)
    equipo.save()

print("Volumenes actualizados")



