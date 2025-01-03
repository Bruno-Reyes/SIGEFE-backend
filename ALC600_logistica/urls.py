from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC600_logistica.views.views import EquipoDisponibleViewSet, EquipoDisponibleCreateView

# Crear router y registrar el ViewSet
router = DefaultRouter()
router.register(r'equipos', EquipoDisponibleViewSet, basename='equipo_disponible')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
    path('crear/', EquipoDisponibleCreateView.as_view(), name='crear-equipo-disponible'),
]
