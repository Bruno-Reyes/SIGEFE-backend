# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC100_captacion.views.views import ConvocatoriaViewSet

router = DefaultRouter()
router.register(r'convocatorias', ConvocatoriaViewSet)
# router.register(r'candidato', ConvocatoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]