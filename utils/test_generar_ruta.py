from ALC200_asignacion.models.models import CentroComunitario
from ALC600_logistica.models.models import CentrosDistribucion
from ALC600_logistica.services import solve_cvrp


estado = 'CIUDAD DE MÉXICO'
 # Obtener el centro de distribución del estado
centro_distribucion = CentrosDistribucion.objects.filter(estado__exact=estado)
centros = CentroComunitario.objects.filter(estado__exact=estado)

solve_cvrp(centro_distribucion, centros)