# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC100_captacion.views.views import CambiarEstadoAceptacion, ConvocatoriaViewSet
from ALC100_captacion.views.views import ConvocatoriasActivas
from ALC100_captacion.views.views import RegistrarCandidato
from ALC100_captacion.views.views import ObtenerActivas
from ALC100_captacion.views.views import DetallesUsuarioListView, DetallesAllUsers, SaS_URL, ConsultarCandidatosInscritos, ConsultarConvocatoriasInscripcion, CambiarAceptacion, DetallesUsuarioPorID

router = DefaultRouter()
router.register(r'convocatorias', ConvocatoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activas/', ConvocatoriasActivas.as_view(), name='convocatoria-list'),
    path('obtener-activas/', ObtenerActivas.as_view(), name='activas-list'),
    path('registrar-candidato/', RegistrarCandidato.as_view(), name='registrar-candidato'),
    path('candidatos/', DetallesUsuarioListView.as_view(), name='lista_candidatos'),
    path('lecs/', DetallesAllUsers.as_view(), name='lista_lecs'),
    path('lec/<int:usuario_id>/', DetallesUsuarioPorID.as_view(), name='lec'),
    path('url-sas/', SaS_URL.as_view(), name='url-sas'),
    path('detalles_usuario/<int:pk>/<str:action>/', CambiarEstadoAceptacion.as_view(), name='cambiar_estado'),
    path('consultar-convocatorias/', ConsultarConvocatoriasInscripcion.as_view(), name='consultar_convocatorias'),
    path('consultar-inscritos-validos/', ConsultarCandidatosInscritos.as_view(), name='consultar_validos'),
    path('cambiar-aceptacion/<int:pk>/<str:action>/', CambiarAceptacion.as_view(), name='cambiar_aceptacion'),
]