# ALC200_asignacion/urls.py
from django.urls import path
from ALC200_asignacion.views.views import (
    LECListView, 
    CentroComunitarioListView, 
    AsignarCentroLEC, 
    EliminarLECView, 
    HistorialLECView, 
    ActualizarTipoUsuario
)

urlpatterns = [
    path('lecs/', LECListView.as_view(), name='lec-list'),  # Ruta para obtener los LEC
    path('centros/', CentroComunitarioListView.as_view(), name='centro-list'),  # Ruta para obtener los centros comunitarios
    path('asignar-lec/', AsignarCentroLEC.as_view(), name='asignar_lec'), # Ruta para asignar un centro a un LEC
    path('eliminar-lec/<int:lec_id>/', EliminarLECView.as_view(), name='eliminar-lec'),
    path('historial-lec/', HistorialLECView.as_view(), name='historial-lec'),  # Ruta para obtener el historial de asignaciones de un LEC por nombre y apellidos
    path('actualizar-tipo-usuario/<int:pk>/', ActualizarTipoUsuario.as_view(), name='actualizar-tipo-usuario')
]
