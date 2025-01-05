from utils.crear_usuarios import crear_usuarios
from utils.crear_convocatorias import crear_convocatorias
from utils.crear_candidatos import crear_candidatos

crear_usuarios()
candidatos = crear_convocatorias() + 100
print('Total vacantes' ,candidatos)
candidatos += 100
crear_candidatos(candidatos)
