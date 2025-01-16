from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC600_logistica.views.views import AsignacionListView, CrearAsignacionView, EquipoDisponibleViewSet, EquipoDisponibleCreateView, ConsultarEstados, GenerarRuta, CentrosPorEstadoAPIView

# Crear router y registrar el ViewSet
router = DefaultRouter()
router.register(r'equipos', EquipoDisponibleViewSet, basename='equipo_disponible')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
    path('crear/', EquipoDisponibleCreateView.as_view(), name='crear-equipo-disponible'),
    path('asignacion/crear/', CrearAsignacionView.as_view(), name='crear-asignacion'),
    path('asignacion/', AsignacionListView.as_view(), name='list_asignaciones'),
    path('consultar-estados/', ConsultarEstados.as_view(), name='consultar-estados'),   
    path('generar-ruta/', GenerarRuta.as_view(), name='generar-ruta'),
    path('obtener-centros/<str:estado>/', CentrosPorEstadoAPIView.as_view(), name='obtener-centros'),
]