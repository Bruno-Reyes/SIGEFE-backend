from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC500_control_escolar.views.views import CalificacionesViewSet, EstudianteViewSet, HistorialMigratorioViewSet

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'calificaciones', CalificacionesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calificaciones/bulk_create/', CalificacionesViewSet.as_view({'post': 'bulk_create'})),
    path('historial_migratorio/', HistorialMigratorioViewSet.as_view({'get': 'list'})),
]