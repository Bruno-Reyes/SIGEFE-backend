from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC400_apoyos_economicos.views.views import (
    PagoApoyoViewSet,
    RegistrarPagoAPIView,
    ListarPagosPorUsuario,
    PagosPendientesAPIView,
)

router = DefaultRouter()
router.register(r'gestion', PagoApoyoViewSet, basename="pagos-gestion")

urlpatterns = [
    path('', include(router.urls)),  # Rutas del ViewSet
    path('registrar/', RegistrarPagoAPIView.as_view(), name="registrar-pago"),
    path('usuario/<int:usuario_id>/', ListarPagosPorUsuario.as_view(), name="listar-pagos-usuario"),
    path('pendientes/', PagosPendientesAPIView.as_view(), name="pagos-pendientes"),
]

