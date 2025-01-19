from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import serializers
from services.send_mail import authenticate, send_mail
from ALC000_sistema_base.models.models import Usuario
from ALC000_sistema_base.serializers import UsuarioSerializer
from utils.mensajes_predefinidos import mensaje_asignacion_beca, mensaje_registro_pago, mensaje_confirmacion_pago, mensaje_rechazo_pago, mensaje_eliminacion_pago
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC400_apoyos_economicos.serializers import PagoApoyoSerializer
from ALC000_sistema_base.models.models import Usuario, TipoUsuario
from ALC400_apoyos_economicos.models.models import ALC004TiposBecas
from ALC400_apoyos_economicos.serializers import ALC004TiposBecasSerializer
from ALC400_apoyos_economicos.models.models import ALC401LecBecas
from ALC400_apoyos_economicos.serializers import ALC401LecBecasSerializer, UsuarioConBecaSerializer, LecBecasSerializer
from ALC100_captacion.models.models import DetallesUsuario
import logging

logger = logging.getLogger(__name__)

class PagoApoyoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de Pagos de Apoyos Económicos.
    """
    queryset = PagoApoyo.objects.all()
    serializer_class = PagoApoyoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrar los pagos según el tipo de usuario autenticado.
        """
        user = self.request.user

        # Si es `coord_nac_rrhh@example.com`, devuelve todos los pagos
        if user.email == "coord_nac_rrhh@example.com":
            return PagoApoyo.objects.all()

        # Si es `LIDER_LEC`, devuelve solo sus pagos
        if user.tipo_usuario == TipoUsuario.LIDER_LEC:
            return PagoApoyo.objects.filter(usuario=user)

        # Otros usuarios no tienen permisos
        return PagoApoyo.objects.none()

    def perform_create(self, serializer):
        """
        Validar que solo `coord_nac_rrhh@example.com` pueda crear pagos.
        """
        user = self.request.user

        if user.email != "coord_nac_rrhh@example.com":
            raise serializers.ValidationError("No tienes permiso para registrar pagos.")

        serializer.save(registrado_por=user.email)

    def update(self, request, *args, **kwargs):
        """
        Sobreescribir para manejar permisos específicos de actualización.
        """
        user = request.user
        instance = self.get_object()

        # Validar permisos para `coord_nac_rrhh@example.com`
        if user.email == "coord_nac_rrhh@example.com":
            # No puede modificar el campo `confirmacion_lec`
            if "confirmacion_lec" in request.data:
                return Response(
                    {"error": "No puedes modificar el campo 'confirmacion_lec'."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Permitir la actualización de otros campos
            return super().update(request, *args, **kwargs)

        # Validar permisos para `LIDER_LEC`
        if user.tipo_usuario == TipoUsuario.LIDER_LEC:
            # Solo puede modificar `confirmacion_lec`
            if set(request.data.keys()) != {"confirmacion_lec"}:
                return Response(
                    {"error": "Solo puedes modificar el campo 'confirmacion_lec'."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Permitir la actualización de `confirmacion_lec`
            instance.confirmacion_lec = request.data.get("confirmacion_lec")
            instance.save()
            return Response(self.get_serializer(instance).data)

        # Si el usuario no tiene permisos
        return Response(
            {"error": "No tienes permiso para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )


    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def pendientes(self, request):
        """
        Endpoint para obtener la lista de pagos pendientes.
        GET: /api/pagos/pendientes/
        """
        pagos_pendientes = self.get_queryset().filter(estatus="pendiente")
        serializer = self.get_serializer(pagos_pendientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrarPagoAPIView(APIView):
    """
    Endpoint independiente para registrar un pago.
    POST: /api/pagos/registrar/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        logger.info(f"Usuario autenticado: {user.email}")

        try:
            # Validar que el usuario autenticado tenga permisos para registrar pagos
            if user.tipo_usuario != "coord_nac_rrhh":
                logger.warning(f"Permiso denegado para el usuario: {user.email}")
                return Response(
                    {"error": f"No tienes permiso para registrar pagos. Usuario: {user.tipo_usuario}"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Validar usuario receptor
            try:
                logger.info(f"Buscando usuario receptor con ID: {request.data['usuario']}")
                usuario_receptor = DetallesUsuario.objects.get(id=request.data["usuario"])
            except DetallesUsuario.DoesNotExist:
                logger.error(f"Usuario receptor no encontrado: {request.data['usuario']}")
                return Response(
                    {"error": "El usuario receptor no existe."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validar que el monto sea mayor a 0
            monto = request.data.get("monto")
            logger.info(f"Monto recibido: {monto}")

            # Validar que el concepto no esté vacío
            concepto = request.data.get("concepto")
            if not concepto:
                logger.warning("El concepto es obligatorio.")
                return Response(
                    {"error": "El concepto es obligatorio."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear el registro del pago
            serializer = PagoApoyoSerializer(data={
                "usuario": usuario_receptor.id,
                "concepto": concepto,
                "monto": monto,
                "estatus": request.data.get("estatus", "pendiente"),
                "registrado_por": user.email,
            }, context={"request": request})

            if serializer.is_valid():
                pago = serializer.save()

                # Obtener información para el correo
                lec_name = usuario_receptor.usuario.email
                destinatario = usuario_receptor.usuario.email

                # Generar el mensaje
                mensaje = mensaje_registro_pago(lec_name, monto)
                #=======================YA ESTA FUNCIONAL=======================
                # Enviar el correo
                try:
                     # Intentar enviar el correo
                    token = authenticate()
                    send_mail(
                        destination=destinatario,
                        subject="Registro de Pago",
                        body=mensaje,
                        token=token
                    )
                    logger.info(f"Pago registrado y correo enviado a: {destinatario}")
                    return Response(
                        {"message": "Pago registrado exitosamente y correo enviado.", "data": serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                except Exception as e:
                    logger.error(f"No se pudo enviar el correo: {str(e)}")
                    return Response(
                        {"error": f"No se pudo enviar el correo: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            logger.warning(f"Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error en RegistrarPagoAPIView: {str(e)}")
            return Response(
                {"error": f"Error en el servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ActualizarMontoPagoAPIView(APIView):
    """
    Endpoint para actualizar el monto de un pago.
    PATCH: /api/pagos/actualizar-monto/<int:id>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            # Obtener el registro de PagoApoyo por ID
            pago = PagoApoyo.objects.get(id=id)
        except PagoApoyo.DoesNotExist:
            return Response({"error": "El registro de pago no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Validar que solo el usuario `coord_nac_rrhh@example.com` pueda modificar el monto
        if request.user.email != "coord_nac_rrhh@example.com":
            return Response(
                {"error": "No tienes permiso para actualizar el monto de este pago."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validar que el monto sea mayor a 0
        nuevo_monto = request.data.get("monto")
        
        # Actualizar el monto y guardar el registro
        pago.monto = nuevo_monto
        pago.save()

        return Response(
            {"message": f"El monto del pago con ID {id} ha sido actualizado a {nuevo_monto}."},
            status=status.HTTP_200_OK
        )

class ListarPagosPorUsuario(APIView):
    """
    Endpoint para listar los pagos de un usuario específico.
    GET: /api/pagos/usuario/<usuario_id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id):
        # Validar que el usuario autenticado pueda acceder a los pagos
        if request.user.email == "coord_nac_rrhh@example.com":
            # `coord_nac_rrhh` puede ver los pagos de cualquier usuario
            pagos = PagoApoyo.objects.filter(usuario_id=usuario_id)
        elif request.user.tipo_usuario == TipoUsuario.LIDER_LEC and request.user.id == usuario_id:
            # Un `LIDER_LEC` solo puede ver sus propios pagos
            pagos = PagoApoyo.objects.filter(usuario=request.user)
        else:
            return Response(
                {"error": "No tienes permiso para ver los pagos de este usuario."},
                status=403
            )

        serializer = PagoApoyoSerializer(pagos, many=True)
        return Response(serializer.data, status=200)

class RechazarPagoAPIView(APIView):
    """
    Endpoint para modificar el campo confirmacion_lec de un registro de PagoApoyo a 'no_recibido'.
    PATCH: /api/pagos/rechazar/<int:id>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            # Obtener el registro de PagoApoyo por ID
            pago = PagoApoyo.objects.get(id=id)
        except PagoApoyo.DoesNotExist:
            return Response(
                {"error": "El registro de pago no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar el campo confirmacion_lec a 'no_recibido'
        pago.confirmacion_lec = 'no_recibido'
        pago.save()

        # Obtener información para el correo - Corregido para acceder al email correctamente
        lec_name = pago.usuario.usuario.email  # Accedemos al email a través de la relación
        monto = pago.monto
        destinatario = pago.usuario.usuario.email  # Accedemos al email a través de la relación

        # Generar el mensaje
        mensaje = mensaje_rechazo_pago(lec_name, monto)

        # Enviar el correo
        #=======================YA ESTA FUNCIONAL=======================
        try:
            token = authenticate()
            send_mail(
                destination=destinatario,
                subject="Rechazo de Pago",
                body=mensaje,
                token=token
            )
            return Response(
                {"message": f"El pago con ID {id} ha sido rechazado y el correo fue enviado."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
class ConfirmarPagoAPIView(APIView):
    """
    Endpoint para modificar el campo confirmacion_lec de un registro de PagoApoyo a 'recibido'.
    PATCH: /api/pagos/confirmar/<int:id>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            # Obtener el registro de PagoApoyo por ID
            pago = PagoApoyo.objects.get(id=id)
        except PagoApoyo.DoesNotExist:
            return Response(
                {"error": "El registro de pago no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar el campo confirmacion_lec a 'recibido'
        pago.confirmacion_lec = 'recibido'
        pago.save()

        # Obtener información para el correo - Corregido para acceder al email correctamente
        lec_name = pago.usuario.usuario.email  # Accedemos al email a través de la relación
        monto = pago.monto
        destinatario = pago.usuario.usuario.email  # Accedemos al email a través de la relación

        # Generar el mensaje
        mensaje = mensaje_confirmacion_pago(lec_name, monto)

        # Enviar el correo
        #=======================YA ESTA FUNCIONAL=======================
        try:
            token = authenticate()
            send_mail(
                destination=destinatario,
                subject="Confirmación de Pago",
                body=mensaje,
                token=token
            )
            return Response(
                {"message": f"El pago con ID {id} ha sido confirmado y el correo fue enviado."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PagosPendientesAPIView(APIView):
    """
    Endpoint para obtener la lista de pagos pendientes, incluyendo el nombre del usuario.
    GET: /api/pagos/pendientes/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Filtrar los pagos pendientes según el usuario
            if request.user.email == "coord_nac_rrhh@example.com":
                # Para coord_nac_rrhh, mostrar todos los pagos pendientes
                pagos_pendientes = PagoApoyo.objects.filter(
                    estatus="pendiente"
                ).select_related('usuario')
            elif request.user.tipo_usuario == TipoUsuario.LIDER_LEC:
                # Para LIDER_LEC, mostrar solo sus pagos pendientes
                # Primero obtener el DetallesUsuario asociado
                try:
                    detalles_usuario = request.user.detalles
                    pagos_pendientes = PagoApoyo.objects.filter(
                        usuario=detalles_usuario,
                        estatus="pendiente"
                    ).select_related('usuario')
                except DetallesUsuario.DoesNotExist:
                    return Response(
                        {"error": "No se encontraron detalles para este usuario."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {"error": "No tienes permiso para acceder a los pagos pendientes."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Serializar los datos incluyendo el nombre del usuario
            data = []
            for pago in pagos_pendientes:
                data.append({
                    "id": pago.id,
                    "usuario_id": pago.usuario.id,
                    "nombre_usuario": f"{pago.usuario.nombres} {pago.usuario.apellido_paterno} {pago.usuario.apellido_materno}",
                    "concepto": pago.concepto,
                    "monto": float(pago.monto),  # Convertir a float para serialización JSON
                    "fecha_pago": pago.fecha_pago,
                    "estatus": pago.estatus,
                    "registrado_por": pago.registrado_por,
                    "confirmacion_lec": pago.confirmacion_lec,
                })

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al obtener pagos pendientes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ALC004TiposBecasListView(APIView):
    def get(self, request):
        tipos_becas = ALC004TiposBecas.objects.all()
        serializer = ALC004TiposBecasSerializer(tipos_becas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class LideresConBecasAPIView(APIView):
    """
    Endpoint para obtener los usuarios tipo 'lider_lec' junto con la beca asignada.
    GET: /api/pagos/lideres-lec-con-becas/
    """
    def get(self, request):
        try:
            # Modificar la consulta para obtener solo usuarios con becas asignadas
            usuarios = Usuario.objects.filter(
                tipo_usuario='lider_lec',
                detalles__isnull=False,
                becas__isnull=False  # Asegurarse de que tengan becas asignadas
            ).select_related(
                'detalles'
            ).prefetch_related(
                'becas__tipo_beca'
            ).distinct()  # Evitar duplicados si tienen múltiples becas

            data = []
            for usuario in usuarios:
                try:
                    if not hasattr(usuario, 'detalles') or not usuario.detalles:
                        continue

                    nombre_completo = f"{usuario.detalles.nombres} {usuario.detalles.apellido_paterno} {usuario.detalles.apellido_materno}".strip()
                    
                    # Obtener la beca activa del usuario
                    beca = usuario.becas.first()
                    if not beca or not hasattr(beca, 'tipo_beca'):
                        continue  # Saltar si no tiene beca o tipo de beca

                    # Solo agregar usuarios que tengan nombre completo y beca asignada
                    if nombre_completo:
                        data.append({
                            "usuario": usuario.detalles.id,
                            "nombre_completo": nombre_completo,
                            "email": usuario.email,
                            "tipo_usuario": usuario.tipo_usuario,
                            "tipo_beca": {
                                "tipo": beca.tipo_beca.tipo
                            }
                        })

                except Exception as e:
                    print(f"Error procesando usuario {usuario.email}: {str(e)}")
                    continue

            # Ordenar por nombre_completo
            data = sorted(data, key=lambda x: x['nombre_completo'])

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error en LideresConBecasAPIView: {str(e)}")
            return Response(
                {"error": f"Error al obtener usuarios con becas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AsignarBecaView(APIView):
    """
    Endpoint para asignar una beca a un usuario y enviar un correo de notificación.
    POST: /api/pagos/asignar-beca/
    """
    def post(self, request):
        try:
            # Obtener y validar los datos
            tipo_beca_id = request.data.get('tipo_beca')
            usuario_id = request.data.get('usuario')
            estatus = request.data.get('estatus', 1)

            if not tipo_beca_id or not usuario_id:
                return Response(
                    {"error": "Tipo de beca y usuario son requeridos"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener el usuario y tipo de beca
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                tipo_beca = ALC004TiposBecas.objects.get(id=tipo_beca_id)
            except (Usuario.DoesNotExist, ALC004TiposBecas.DoesNotExist) as e:
                return Response(
                    {"error": "Usuario o tipo de beca no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Crear la asignación de beca
            beca = ALC401LecBecas.objects.create(
                tipo_beca=tipo_beca,
                usuario=usuario,
                estatus=estatus
            )

            # Crear el registro en PagoApoyo
            try:
                PagoApoyo.objects.create(
                    usuario=usuario.detalles,
                    concepto=tipo_beca.tipo,
                    monto=tipo_beca.monto,
                    estatus='pendiente',
                    registrado_por=request.user.email
                )
            except Exception as e:
                return Response(
                    {"error": f"Error al crear el registro de pago: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Enviar correo de notificación
        #=======================YA ESTA FUNCIONAL=======================
            try:
                token = authenticate()
                send_mail(
                    destination=usuario.email,
                    subject="Asignación de Beca",
                    body=mensaje_asignacion_beca(usuario.email, tipo_beca.tipo),
                    token=token
                )
            except Exception as e:
                # Log el error pero no detener el proceso
                print(f"Error al enviar correo: {str(e)}")

            return Response(
                {"message": "Beca asignada exitosamente"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class LecBecasListView(generics.ListAPIView):
    queryset = ALC401LecBecas.objects.select_related('tipo_beca', 'usuario').all()
    serializer_class = LecBecasSerializer
    
class LecBecasPorUsuarioView(generics.ListAPIView):
    """
    Endpoint para obtener las becas asignadas a un usuario específico por su `usuario_id`.
    GET: /api/lec-becas/<int:usuario_id>/
    """
    serializer_class = LecBecasSerializer

    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']
        return ALC401LecBecas.objects.filter(usuario_id=usuario_id).select_related('tipo_beca', 'usuario')
    
    
class EditarAsignacionBecaAPIView(APIView):
    """
    Endpoint para editar la asignación de beca de un usuario.
    PATCH: /api/lec-becas/editar/<int:usuario_id>/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, usuario_id):
        try:
            # Buscar la asignación de beca del usuario
            asignacion_beca = ALC401LecBecas.objects.get(usuario_id=usuario_id)
        except ALC401LecBecas.DoesNotExist:
            return Response(
                {"error": "No se encontró una asignación de beca para este usuario."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que el tipo de beca proporcionado existe
        tipo_beca_id = request.data.get("tipo_beca_id")
        if not tipo_beca_id:
            return Response({"error": "El campo 'tipo_beca_id' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tipo_beca = ALC004TiposBecas.objects.get(id=tipo_beca_id)
        except ALC004TiposBecas.DoesNotExist:
            return Response({"error": "El tipo de beca proporcionado no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar la asignación de beca
        asignacion_beca.tipo_beca = tipo_beca
        asignacion_beca.save()

        # Obtener información para el correo
        lec_name = asignacion_beca.usuario.email
        tipo_beca_nombre = tipo_beca.tipo
        destinatario = asignacion_beca.usuario.email

        # Generar el mensaje
        mensaje = mensaje_asignacion_beca(lec_name, tipo_beca_nombre)

        # Enviar el correo
        #=======================YA ESTA FUNCIONAL=======================
        try:
            token = authenticate()
            send_mail(
                destination=destinatario,
                subject="Actualización de Asignación de Beca",
                body=mensaje,
                token=token
            )
            return Response(
                {"message": f"La asignación de beca del usuario con ID {usuario_id} ha sido actualizada y el correo fue enviado."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class EliminarPagoAPIView(APIView):
    """
    Endpoint para eliminar un registro de PagoApoyo.
    DELETE: /api/pagos/eliminar/<int:id>/
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            # Obtener el registro de PagoApoyo por ID
            pago = PagoApoyo.objects.get(id=id)
        except PagoApoyo.DoesNotExist:
            return Response({"error": "El registro de pago no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Validar permisos: solo `coord_nac_rrhh@example.com` puede eliminar pagos
        if request.user.email != "coord_nac_rrhh@example.com":
            return Response(
                {"error": "No tienes permiso para eliminar registros de pago."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Obtener información para el correo antes de eliminar
            # Accedemos al email a través de la relación usuario -> detalles -> usuario
            lec_name = pago.usuario.usuario.email  # Corregido: accedemos al email a través de la relación
            monto = pago.monto
            destinatario = pago.usuario.usuario.email  # Corregido: accedemos al email a través de la relación

            # Eliminar el registro de la base de datos
            pago.delete()

            # Generar y enviar el mensaje de notificación
            mensaje = mensaje_eliminacion_pago(lec_name, monto)
            try:
                token = authenticate()
                send_mail(
                    destination=destinatario,
                    subject="Eliminación de Pago",
                    body=mensaje,
                    token=token
                )
                return Response(
                    {"message": f"El pago con ID {id} ha sido eliminado y el correo fue enviado."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                # Si falla el envío del correo, al menos notificamos que el pago fue eliminado
                return Response(
                    {
                        "message": f"El pago con ID {id} ha sido eliminado pero no se pudo enviar el correo.",
                        "error_correo": str(e)
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"error": f"Error al procesar la eliminación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )