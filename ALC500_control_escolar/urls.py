from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC500_control_escolar.views.views import CalificacionesViewSet, EstudianteViewSet, HistorialMigratorioView, ReinscribirEstudianteView

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'calificaciones', CalificacionesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calificaciones/bulk_create/', CalificacionesViewSet.as_view({'post': 'bulk_create'})),
    path('historial_migratorio/', HistorialMigratorioView.as_view(), name='historial_migratorio'),
    path('reinscribir_estudiante/', ReinscribirEstudianteView.as_view(), name='reinscribir_estudiante'),
    path('reinscribir_estudiante/<int:id_estudiante>/', ReinscribirEstudianteView.as_view(), name='reinscribir_estudiante_get'),
]