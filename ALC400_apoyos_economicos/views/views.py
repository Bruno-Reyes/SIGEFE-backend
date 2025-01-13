from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ALC000_sistema_base.models.models import Usuario
from ALC000_sistema_base.serializers import UsuarioSerializer
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
        print(user)

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
            serializer.save()
            return Response(
                {"message": "Pago registrado exitosamente.", "data": serializer.data},
                status=status.HTTP_201_CREATED
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
            return Response({"error": "El registro de pago no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar el campo confirmacion_lec a 'no_recibido'
        pago.confirmacion_lec = 'no_recibido'
        pago.save()

        return Response({"message": f"El pago con ID {id} ha sido rechazado."}, status=status.HTTP_200_OK)
    
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
            return Response({"error": "El registro de pago no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar el campo confirmacion_lec a 'recibido'
        pago.confirmacion_lec = 'recibido'
        pago.save()

        return Response({"message": f"El pago con ID {id} ha sido confirmado."}, status=status.HTTP_200_OK)

class PagosPendientesAPIView(APIView):
    """
    Endpoint para obtener la lista de pagos pendientes.
    GET: /api/pagos/pendientes/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtrar los pagos pendientes según el usuario
        if request.user.email == "coord_nac_rrhh@example.com":
            # `coord_nac_rrhh` puede ver todos los pagos pendientes
            pagos_pendientes = PagoApoyo.objects.filter(estatus="pendiente")
        elif request.user.tipo_usuario == TipoUsuario.LIDER_LEC:
            # Un `LIDER_LEC` solo puede ver sus pagos pendientes
            pagos_pendientes = PagoApoyo.objects.filter(usuario=request.user, estatus="pendiente")
        else:
            return Response(
                {"error": "No tienes permiso para acceder a los pagos pendientes."},
                status=403
            )

        serializer = PagoApoyoSerializer(pagos_pendientes, many=True)
        return Response(serializer.data, status=200)


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
    def post(self, request):
        serializer = ALC401LecBecasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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