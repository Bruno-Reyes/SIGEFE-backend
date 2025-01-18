# ALC200_asignacion/urls.py
from django.urls import path
from ALC300_capacitacion.views.views import (
    registrar_plan_capacitacion, 
    obtener_lecs_pendientes, 
    registrar_asistencia,
    obtener_progreso_lec,
    consultar_capacitacion_lec
)

urlpatterns = [
    path('registrar-plan/', registrar_plan_capacitacion, name='registrar_plan_capacitacion'),
    path('lecs-pendientes/', obtener_lecs_pendientes, name='obtener_lecs_pendientes'),
    path('registrar-asistencia/', registrar_asistencia, name='registrar_asistencia'),
    path('progreso-lec/', obtener_progreso_lec, name='obtener_progreso_lec'),
    path('consultar_capacitacion_lec/', consultar_capacitacion_lec, name='consultar_capacitacion_lec'),
]
