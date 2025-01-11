from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ALC500_control_escolar.views.views import EstudianteViewSet

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]