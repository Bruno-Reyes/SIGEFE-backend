from utils.crear_usuarios import crear_usuarios
from utils.crear_convocatorias import crear_convocatorias
from utils.crear_candidatos import crear_candidatos

crear_usuarios()
total_participantes = crear_convocatorias()
crear_candidatos(int(total_participantes*1.25))