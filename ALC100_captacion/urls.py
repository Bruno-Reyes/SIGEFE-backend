# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC100_captacion.views.views import ConvocatoriaViewSet
from ALC100_captacion.views.views import ConvocatoriasActivas
from ALC100_captacion.views.views import RegistrarCandidato
from ALC100_captacion.views.views import ObtenerActivas
from ALC100_captacion.views.views import ObtenerAspirantes

router = DefaultRouter()
router.register(r'convocatorias', ConvocatoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activas/', ConvocatoriasActivas.as_view(), name='convocatoria-list'),
    path('obtener-activas/', ObtenerActivas.as_view(), name='activas-list'),
    path('registrar-candidato/', RegistrarCandidato.as_view(), name='registrar-candidato'),
    path('obtener-aspirantes-validacion/', ObtenerAspirantes.as_view(), name='obtener-aspirantes-validacion'),
]