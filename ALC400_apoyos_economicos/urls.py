from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC400_apoyos_economicos.views.views import (
    PagoApoyoViewSet,
    RegistrarPagoAPIView,
    ListarPagosPorUsuario,
    PagosPendientesAPIView,
    ALC004TiposBecasListView,
    LideresConBecasAPIView,
    AsignarBecaView,
    RechazarPagoAPIView,
    ConfirmarPagoAPIView,
    LecBecasListView,
    LecBecasPorUsuarioView,
    ActualizarMontoPagoAPIView,
    EditarAsignacionBecaAPIView,
    EliminarPagoAPIView
)

router = DefaultRouter()
router.register(r'gestion', PagoApoyoViewSet, basename="pagos-gestion")

urlpatterns = [
    path('', include(router.urls)),  # Rutas del ViewSet
    path('registrar/', RegistrarPagoAPIView.as_view(), name="registrar-pago"),
    path('usuario/<int:usuario_id>/', ListarPagosPorUsuario.as_view(), name="listar-pagos-usuario"),
    path('pendientes/', PagosPendientesAPIView.as_view(), name="pagos-pendientes"),
    path('tipos_becas/', ALC004TiposBecasListView.as_view(), name='tipos-becas-list'),
    path('lideres-lec-con-becas/', LideresConBecasAPIView.as_view(), name='lideres_lec_con_becas'),
    path('beca-lec/<int:usuario_id>/', LecBecasPorUsuarioView.as_view(), name='lec_con_beca'),
    path('asignar-beca/', AsignarBecaView.as_view(), name='asignar_beca'),
    path('rechazar/<int:id>/', RechazarPagoAPIView.as_view(), name='rechazar_pago'),
    path('confirmar/<int:id>/', ConfirmarPagoAPIView.as_view(), name='confirmar_pago'),
    path('actualizar-monto/<int:id>/', ActualizarMontoPagoAPIView.as_view(), name='actualizar_monto_pago'),
    path('editar/<int:usuario_id>/', EditarAsignacionBecaAPIView.as_view(), name='editar_asignacion_beca'),
    path('eliminar/<int:id>/', EliminarPagoAPIView.as_view(), name='eliminar_pago'),
]