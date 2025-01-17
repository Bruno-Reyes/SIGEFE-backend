from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ALC200_asignacion.models.models import CentroComunitario, LEC
from ALC300_capacitacion.models.models import PlanCapacitacion
from ALC300_capacitacion.serializers import PlanCapacitacionSerializer
import json

@api_view(['POST'])
def registrar_plan_capacitacion(request):
    data = request.data
    centro_id = data.get('centro_id')
    lecs_ids = data.get('lecs_ids')
    num_sesiones = data.get('num_sesiones')
    modalidad = data.get('modalidad')
    fechas_sesiones = data.get('fechas_sesiones')

    try:
        centro = CentroComunitario.objects.get(id=centro_id)
        lecs = LEC.objects.filter(id__in=lecs_ids)
        plan = PlanCapacitacion.objects.create(
            centro=centro,
            num_sesiones=num_sesiones,
            modalidad=modalidad,
            fechas_sesiones=fechas_sesiones
        )
        plan.lecs.set(lecs)
        plan.save()
        return Response({'message': 'Plan de capacitación registrado exitosamente.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_lecs_pendientes(request):
    centro_id = request.query_params.get('centro_id')
    try:
        centro = CentroComunitario.objects.get(id=centro_id)
        planes = PlanCapacitacion.objects.filter(centro=centro)
        lecs_data = []
        for plan in planes:
            for lec in plan.lecs.all():
                lec_data = {
                    'id': lec.id,
                    'nombre': f"{lec.nombre} {lec.apellido_paterno} {lec.apellido_materno}",
                    'numSesiones': plan.num_sesiones,
                    'modalidad': plan.modalidad,
                    'fechasSesiones': plan.fechas_sesiones,
                }
                # Agregar calificaciones y asistencias si existen
                if str(lec.id) in plan.calificaciones:
                    for sesion, calificacion in plan.calificaciones[str(lec.id)].items():
                        lec_data[f'S{int(sesion) + 1}'] = calificacion
                if str(lec.id) in plan.asistencias:
                    for sesion, asistencia in plan.asistencias[str(lec.id)].items():
                        lec_data[f'Asistencia{int(sesion) + 1}'] = asistencia
                
                lecs_data.append(lec_data)
        return Response(lecs_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def registrar_asistencia(request):
    data = request.data
    lecs = data.get('lecs', [])
    print("Datos recibidos:", lecs)

    try:
        for lec_data in lecs:
            lec_id = lec_data.get('id')
            calificaciones = {}
            asistencias = {}
            
            for key, value in lec_data.items():
                if key.startswith('S'):
                    sesion_num = int(key[1:]) - 1
                    calificaciones[str(sesion_num)] = value
                elif key.startswith('Asistencia'):
                    sesion_num = int(key[10:]) - 1
                    asistencias[str(sesion_num)] = value

            lec = LEC.objects.get(id=lec_id)
            plan = PlanCapacitacion.objects.filter(lecs=lec).first()
            
            if plan:
                # Actualizar calificaciones y asistencias
                plan_calificaciones = plan.calificaciones or {}
                plan_asistencias = plan.asistencias or {}
                
                # Actualizar con los nuevos datos
                plan_calificaciones[str(lec_id)] = calificaciones
                plan_asistencias[str(lec_id)] = asistencias
                
                plan.calificaciones = plan_calificaciones
                plan.asistencias = plan_asistencias
                plan.save()

        return Response({'message': 'Asistencia registrada exitosamente.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
