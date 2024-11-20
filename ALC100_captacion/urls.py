# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC000_sistema_base.views.views import ConvocatoriaViewSet

router = DefaultRouter()
router.register(r'convocatorias', ConvocatoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]