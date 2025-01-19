from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ALC200_asignacion.models.models import CentroComunitario, LEC
from ALC300_capacitacion.models.models import PlanCapacitacion
from ALC300_capacitacion.serializers import PlanCapacitacionSerializer
import json
import logging
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)

@api_view(['POST'])
def registrar_plan_capacitacion(request):
    
    data = request.data
    centro_id = data.get('centro_id')
    lecs_ids = data.get('lecs_ids')
    num_sesiones = data.get('num_sesiones')
    modalidad = data.get('modalidad')
    fechas_sesiones = data.get('fechas_sesiones')
    tipo_capacitacion = data.get('tipo_capacitacion')  # Obtener tipo de capacitación

    try:
        # Validar fechas de sesiones
        fecha_actual = timezone.now()
        
        # Convertir fechas ISO a objetos datetime y validar orden
        fechas_ordenadas = []
        for i, fecha in enumerate(fechas_sesiones):
            fecha_sesion = datetime.strptime(fecha.split('T')[0], '%Y-%m-%d')
            
            # Validar que la fecha no sea anterior a la actual
            if fecha_sesion.date() < fecha_actual.date():
                return Response({
                    'error': f'La sesión {i+1} ({fecha.split("T")[0]}) es anterior a la fecha actual'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar orden cronológico
            if i > 0 and fecha_sesion <= datetime.strptime(fechas_sesiones[i-1].split('T')[0], '%Y-%m-%d'):
                return Response({
                    'error': f'La sesión {i+1} debe ser posterior a la sesión {i}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            fechas_ordenadas.append(fecha)

        # Verificar que los LECs no tengan planes activos
        lecs_con_planes_activos = []
        for lec_id in lecs_ids:
            planes_activos = PlanCapacitacion.objects.filter(
                lecs__id=lec_id,
                estado=True
            )
            if planes_activos.exists():
                lec = LEC.objects.get(id=lec_id)
                lecs_con_planes_activos.append(f"{lec.nombre} {lec.apellido_paterno}")

        if lecs_con_planes_activos:
            return Response({
                'error': f'Los siguientes LECs tienen planes de capacitación activos: {", ".join(lecs_con_planes_activos)}',
                'lecs_con_planes': lecs_con_planes_activos
            }, status=status.HTTP_400_BAD_REQUEST)

        # Si no hay planes activos, proceder con la creación
        centro = CentroComunitario.objects.get(id=centro_id)
        lecs = LEC.objects.filter(id__in=lecs_ids)
        plan = PlanCapacitacion.objects.create(
            centro=centro,
            num_sesiones=num_sesiones,
            modalidad=modalidad,
            fechas_sesiones=fechas_ordenadas,  # Guardar fechas validadas
            tipo_capacitacion=tipo_capacitacion  # Guardar tipo de capacitación
        )
        plan.lecs.set(lecs)
        plan.save()
        return Response({'message': 'Plan de capacitación registrado exitosamente.'}, status=status.HTTP_201_CREATED)
    except json.JSONDecodeError:
        return Response({'error': 'Formato de fechas inválido'}, status=status.HTTP_400_BAD_REQUEST)
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
                    'estado': plan.estado
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
            
            # Primero recolectamos todas las asistencias y calificaciones
            for key, value in lec_data.items():
                if key.startswith('S'):
                    sesion_num = int(key[1:]) - 1
                    calificaciones[str(sesion_num)] = value
                elif key.startswith('Asistencia'):
                    sesion_num = int(key[10:]) - 1
                    asistencias[str(sesion_num)] = value
            
            # Validar que cada asistencia marcada como True tenga su calificación
            for sesion_num, asistencia in asistencias.items():
                if asistencia and str(sesion_num) not in calificaciones:
                    return Response(
                        {'error': f'La sesión {int(sesion_num) + 1} tiene asistencia pero no tiene calificación'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if asistencia and calificaciones[str(sesion_num)] is None:
                    return Response(
                        {'error': f'La sesión {int(sesion_num) + 1} tiene asistencia pero no tiene calificación'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            lec = LEC.objects.get(id=lec_id)
            plan = PlanCapacitacion.objects.filter(lecs=lec).first()
            
            if plan:
                # Actualizar calificaciones y asistencias
                plan_calificaciones = plan.calificaciones or {}
                plan_asistencias = plan.asistencias or {}
                
                # Actualizar con los nuevos datos
                plan_calificaciones[str(lec_id)] = calificaciones
                plan_asistencias[str(lec_id)] = asistencias

                # Verificar si todas las asistencias están marcadas como true
                todas_asistencias = True
                for lec_asistencias in plan_asistencias.values():
                    if not todas_asistencias:
                        break
                    for asistencia in lec_asistencias.values():
                        if not asistencia:
                            todas_asistencias = False
                            break

                # Actualizar el estado del plan si todas las asistencias son true
                if todas_asistencias:
                    plan.estado = False
                
                plan.save()

        return Response({'message': 'Asistencia y calificaciones registradas exitosamente.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_progreso_lec(request):
    centro_id = request.query_params.get('centro_id')
    logger.info(f"Recibida solicitud de progreso para centro_id: {centro_id}")
    
    try:
        # Verificar si se recibió el centro_id
        if not centro_id:
            logger.error("No se proporcionó centro_id en la solicitud")
            return Response(
                {'error': 'centro_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el Centro Comunitario
        try:
            centro = CentroComunitario.objects.get(id=centro_id)
            logger.info(f"Centro encontrado: {centro.id}")
        except CentroComunitario.DoesNotExist:
            logger.error(f"No se encontró Centro con id: {centro_id}")
            return Response(
                {'error': f'No se encontró Centro con id: {centro_id}'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar planes de capacitación
        planes = PlanCapacitacion.objects.filter(centro=centro)
        logger.info(f"Planes encontrados: {planes.count()}")

        progreso_data = []
        for plan in planes:
            logger.info(f"Procesando plan {plan.id}")
            for lec in plan.lecs.all():
                asistencias = plan.asistencias.get(str(lec.id), {})
                calificaciones_dict = plan.calificaciones.get(str(lec.id), {})
                
                # Convertir el diccionario de calificaciones a una lista ordenada
                calificaciones = []
                for i in range(plan.num_sesiones):
                    calificaciones.append(calificaciones_dict.get(str(i), None))
                
                # Calcular asistencias y promedio
                num_asistencias = sum(1 for asistencia in asistencias.values() if asistencia)
                porcentaje_progreso = (num_asistencias / plan.num_sesiones) * 100 if plan.num_sesiones > 0 else 0
                
                calificaciones_valores = [cal for cal in calificaciones if cal is not None]
                promedio = sum(calificaciones_valores) / len(calificaciones_valores) if calificaciones_valores else 0

                plan_data = {
                    'id': plan.id,
                    'nombre': f"{lec.nombre} {lec.apellido_paterno} {lec.apellido_materno}",
                    'tipo_capacitacion': plan.tipo_capacitacion,
                    'num_sesiones': plan.num_sesiones,
                    'asistencias': num_asistencias,
                    'progreso': round(porcentaje_progreso, 2),
                    'calificaciones': calificaciones,
                    'promedio': round(promedio, 2)
                }
                progreso_data.append(plan_data)

        return Response(progreso_data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def consultar_capacitacion_lec(request):
    email = request.query_params.get('email')
    logger.info(f"Recibida solicitud de progreso para email: {email}")
    
    try:
        # Verificar si se recibió el email
        if not email:
            logger.error("No se proporcionó email en la solicitud")
            return Response(
                {'error': 'Email es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el LEC
        try:
            lec = LEC.objects.get(email=email)
            logger.info(f"LEC encontrado: {lec.id}")
        except LEC.DoesNotExist:
            logger.error(f"No se encontró LEC con email: {email}")
            return Response(
                {'error': f'No se encontró LEC con email: {email}'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar planes de capacitación
        planes = PlanCapacitacion.objects.filter(lecs=lec)
        logger.info(f"Planes encontrados: {planes.count()}")

        progreso_data = []
        for plan in planes:
            logger.info(f"Procesando plan {plan.id}")
            asistencias = plan.asistencias.get(str(lec.id), {})
            calificaciones_dict = plan.calificaciones.get(str(lec.id), {})
            
            # Convertir el diccionario de calificaciones a una lista ordenada
            calificaciones = []
            for i in range(plan.num_sesiones):
                calificaciones.append(calificaciones_dict.get(str(i), None))
            
            # Calcular asistencias y promedio
            num_asistencias = sum(1 for asistencia in asistencias.values() if asistencia)
            porcentaje_progreso = (num_asistencias / plan.num_sesiones) * 100 if plan.num_sesiones > 0 else 0
            
            calificaciones_valores = [cal for cal in calificaciones if cal is not None]
            promedio = sum(calificaciones_valores) / len(calificaciones_valores) if calificaciones_valores else 0

            plan_data = {
                'id': plan.id,
                'centro': f"{plan.centro.clave_centro_trabajo}",
                'modalidad': plan.modalidad,
                'num_sesiones': plan.num_sesiones,
                'fechas_sesiones': plan.fechas_sesiones,
                'asistencias': asistencias,
                'calificaciones': calificaciones,  # Ahora es una lista ordenada
                'progreso': round(porcentaje_progreso, 2),
                'promedio': round(promedio, 2),
                'tipo_capacitacion': plan.tipo_capacitacion  
            }
            progreso_data.append(plan_data)

        return Response(progreso_data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}", exc_info=True)

        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
