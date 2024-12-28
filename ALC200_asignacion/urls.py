# ALC200_asignacion/urls.py
from django.urls import path
from ALC200_asignacion.views.views import LECListView

urlpatterns = [
    path('lecs/', LECListView.as_view(), name='lec-list'),  # Ruta para obtener los LEC
]
