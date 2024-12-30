# ALC200_asignacion/urls.py
from django.urls import path
from ALC200_asignacion.views.views import LECListView, CentroComunitarioListView

urlpatterns = [
    path('lecs/', LECListView.as_view(), name='lec-list'),  # Ruta para obtener los LEC
    path('centros/', CentroComunitarioListView.as_view(), name='centro-list'),  # Ruta para obtener los centros comunitarios
]
