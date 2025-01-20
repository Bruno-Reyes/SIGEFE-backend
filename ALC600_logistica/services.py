import googlemaps
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from decouple import config

from ALC600_logistica.models.models import AsignacionMaterial

API_KEY = config('GOOGLE_MAPS_API_KEY')

# Inicializa el cliente de Google Maps
gmaps = googlemaps.Client(key=API_KEY)

def get_distance_matrix(locations):
    """
    Obtiene la matriz de distancias reales utilizando la Google Distance Matrix API.
    Divide las llamadas en bloques de 10 para manejar limitaciones de la API.

    locations: Lista de coordenadas [(lat, lng), ...].
    Retorna:
        distance_matrix: Matriz de distancias (en metros) entre todas las ubicaciones.
    """
    # Convertir las coordenadas a strings para la API
    location_strings = [f"{lat},{lng}" for lat, lng in locations]

    # Tamaño máximo de bloque (Google permite hasta 100 elementos por solicitud)
    chunk_size = 10
    n = len(location_strings)

    # Inicializar la matriz de distancias con ceros
    distance_matrix = [[0 for _ in range(n)] for _ in range(n)]

    # Dividir las ubicaciones en bloques para orígenes y destinos
    for i in range(0, n, chunk_size):
        origins_chunk = location_strings[i:i + chunk_size]
        for j in range(0, n, chunk_size):
            destinations_chunk = location_strings[j:j + chunk_size]

            # Llamada a la API para el bloque actual
            matrix = gmaps.distance_matrix(
                origins=origins_chunk,
                destinations=destinations_chunk,
                mode="driving",
                units="metric"
            )

            # Obtener las distancias del bloque y actualizarlas en la matriz principal
            for origin_index, row in enumerate(matrix['rows']):
                for destination_index, element in enumerate(row['elements']):
                    global_origin_index = i + origin_index
                    global_destination_index = j + destination_index
                    
                    # Asegurarse de no exceder los índices
                    if global_origin_index < n and global_destination_index < n:
                        distance_matrix[global_origin_index][global_destination_index] = element['distance']['value']

    return distance_matrix


# **Paso 2: Crear el problema**
def create_data_model(centro_distribucion, centros_comunitarios):
    data = {}
    # Coordenadas de las localidades (incluido el centro de distribución como nodo 0)
    data['locations'] = [
        (float(centro_distribucion.latitud), float(centro_distribucion.longitud)),  # Centro distribución
    ]
    
    data['id'] = [-1]
    
    for localidad in centros_comunitarios:
        data['locations'].append((float(localidad.latitud), float(localidad.longitud)))
        data['id'].append(localidad.id)
    
    
    
    
    # Nodo inicial para todos los vehículos (el centro de distribución)
    data['depot'] = 0
    
    # Obtener la matriz de distancias reales
    data['distance_matrix'] = get_distance_matrix(data['locations'])
    return data

def solve_tsp_ortools(distance_matrix):
    n = len(distance_matrix)
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        index = routing.Start(0)
        path = []
        cost = 0
        while not routing.IsEnd(index):
            path.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            cost += routing.GetArcCostForVehicle(previous_index,index, 0)
        path.append(manager.IndexToNode(index))
        return path, cost
    else:
        return None, None


# **Paso 3: Resolver el CVRP**
def solve_cvrp(centro_distribucion, centros_comunitarios):
    data = create_data_model(centro_distribucion[0], centros_comunitarios)
    path, cost = solve_tsp_ortools(data['distance_matrix'])
    # Crear ruta de distribución usando coordenadas
    route = [data['id'][i] for i in path]
    return route, cost