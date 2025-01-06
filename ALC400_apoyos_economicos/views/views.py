from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import serializers
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC400_apoyos_economicos.serializers import PagoApoyoSerializer
from ALC000_sistema_base.models.models import Usuario, TipoUsuario


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
        
        # Si es `coord_nac_rrhh@example.com`, devuelve todos los pagos
        if user.email == "dep_finanzas@example.com":
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
        
        # Validar permisos para `dep_finanzas@example.com`
        if user.email == "dep_finanzas@example.com":
            # Solo puede modificar `estatus`
            if set(request.data.keys()) != {"estatus"}:
                return Response(
                    {"error": "Solo puedes modificar el campo 'estatus'."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Permitir la actualización de `estatus`
            instance.estatus = request.data.get("estatus")
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

        # Validar que el usuario autenticado sea `coord_nac_rrhh@example.com`
        if user.email != "coord_nac_rrhh@example.com":
            return Response(
                {"error": "No tienes permiso para registrar pagos."},
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

        # Crear el registro del pago
        serializer = PagoApoyoSerializer(data={
            "usuario": usuario_receptor.id,
            "concepto": request.data.get("concepto"),
            "monto": request.data.get("monto"),
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


class PagosPendientesAPIView(APIView):
    """
    Endpoint para obtener la lista de pagos pendientes.
    GET: /api/pagos/pendientes/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtrar los pagos pendientes según el usuario
        if request.user.email == "coord_nac_rrhh@example.com" or request.user.email == "dep_finanzas@example.com" :
            # `coord_nac_rrhh` y `dep_finanzas` pueden ver todos los pagos
            pagos = PagoApoyo.objects.all()
        elif request.user.tipo_usuario == TipoUsuario.LIDER_LEC:
            # Un `LIDER_LEC` solo puede ver sus propios pagos
            pagos = PagoApoyo.objects.filter(usuario=request.user)
        else:
            return Response(
                {"error": "No tienes permiso para acceder a los pagos "},
                status=403
            )

        serializer = PagoApoyoSerializer(pagos, many=True)
        return Response(serializer.data, status=200)
