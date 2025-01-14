from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from services.send_mail import send_mail
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

        # Validar que el usuario autenticado tenga permisos para registrar pagos
        if user.tipo_usuario != "coord_nac_rrhh":
            return Response(
                {"error": f"No tienes permiso para registrar pagos. Usuario: {user.tipo_usuario}"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validar usuario receptor
        try:
            usuario_receptor = Usuario.objects.get(id=request.data["usuario"])
        except Usuario.DoesNotExist:
            return Response(
                {"error": "El usuario receptor no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que el monto sea mayor a 0
        monto = request.data.get("monto")
        if monto is None or float(monto) <= 0:
            return Response(
                {"error": "El monto debe ser mayor a 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el registro del pago
        serializer = PagoApoyoSerializer(data={
            "usuario": usuario_receptor.id,
            "concepto": request.data.get("concepto"),
            "monto": monto,
            "estatus": request.data.get("estatus", "pendiente"),
            "registrado_por": user.email,
        }, context={"request": request})

        if serializer.is_valid():
            pago = serializer.save()

            # Obtener información para el correo
            lec_name = usuario_receptor.email
            destinatario = usuario_receptor.email

            # Generar el mensaje
            mensaje = mensaje_registro_pago(lec_name, monto)

            # Enviar el correo
            try:
                token = request.headers.get('Authorization', '').replace('Bearer ', '')
                send_mail(
                    destination=destinatario,
                    subject="Registro de Pago",
                    body=mensaje,
                    token=token
                )
                return Response(
                    {"message": "Pago registrado exitosamente y correo enviado.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": f"No se pudo enviar el correo: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if not nuevo_monto or float(nuevo_monto) <= 0:
            return Response(
                {"error": "El monto debe ser un número mayor a 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

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

        # Obtener información para el correo
        lec_name = pago.usuario.email
        monto = pago.monto
        destinatario = pago.usuario.email

        # Generar el mensaje
        mensaje = mensaje_rechazo_pago(lec_name, monto)

        # Enviar el correo
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
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

        # Obtener información para el correo
        lec_name = pago.usuario.email
        monto = pago.monto
        destinatario = pago.usuario.email

        # Generar el mensaje
        mensaje = mensaje_confirmacion_pago(lec_name, monto)

        # Enviar el correo
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
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
        # Filtrar los pagos pendientes según el usuario
        if request.user.email == "coord_nac_rrhh@example.com":
            pagos_pendientes = PagoApoyo.objects.filter(estatus="pendiente").select_related('usuario')
        elif request.user.tipo_usuario == TipoUsuario.LIDER_LEC:
            pagos_pendientes = PagoApoyo.objects.filter(usuario=request.user, estatus="pendiente").select_related('usuario')
        else:
            return Response(
                {"error": "No tienes permiso para acceder a los pagos pendientes."},
                status=403
            )

        # Serializar los datos incluyendo el nombre del usuario
        data = [
            {
                "id": pago.id,
                "usuario_id": pago.usuario.id,
                "nombre_usuario": f"{pago.usuario.first_name} {pago.usuario.last_name}",
                "concepto": pago.concepto,
                "monto": pago.monto,
                "fecha_pago": pago.fecha_pago,
                "estatus": pago.estatus,
                "registrado_por": pago.registrado_por,
                "confirmacion_lec": pago.confirmacion_lec,
            }
            for pago in pagos_pendientes
        ]

        return Response(data, status=status.HTTP_200_OK)


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
        # Obtener los usuarios tipo 'lider_lec' y prefetch de las becas
        usuarios = Usuario.objects.filter(tipo_usuario='lider_lec').prefetch_related('becas__tipo_beca')

        # Formatear los datos manualmente
        data = []
        for usuario in usuarios:
            beca_asignada = usuario.becas.first().tipo_beca.tipo if usuario.becas.exists() else None
            data.append({
                "usuario_id": usuario.id,
                "email": usuario.email,
                "tipo_usuario": usuario.tipo_usuario,
                "tipo_beca_asignada": beca_asignada
            })

        return Response(data, status=200)
    
class AsignarBecaView(APIView):
    """
    Endpoint para asignar una beca a un usuario y enviar un correo de notificación.
    POST: /api/lec-becas/asignar/
    """
    def post(self, request):
        serializer = ALC401LecBecasSerializer(data=request.data)
        if serializer.is_valid():
            beca = serializer.save()

            # Obtener información para el correo
            lec_name = beca.usuario.email
            tipo_beca = beca.tipo_beca.tipo
            destinatario = beca.usuario.email

            # Generar el mensaje
            mensaje = mensaje_asignacion_beca(lec_name, tipo_beca)

            # Enviar el correo
            try:
                token = request.headers.get('Authorization', '').replace('Bearer ', '')
                send_mail(
                    destination=destinatario,
                    subject="Asignación de Beca",
                    body=mensaje,
                    token=token
                )
                return Response(
                    {"message": "Beca asignada y correo enviado correctamente.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": f"No se pudo enviar el correo: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
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

        # Obtener información para el correo antes de eliminar
        lec_name = pago.usuario.email
        monto = pago.monto
        destinatario = pago.usuario.email

        # Eliminar el registro de la base de datos
        pago.delete()

        # Generar y enviar el mensaje de notificación
        mensaje = mensaje_eliminacion_pago(lec_name, monto)
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
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
            return Response(
                {"error": f"No se pudo enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )