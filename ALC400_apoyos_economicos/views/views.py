from django.shortcuts import render

# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from django.utils import timezone
from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC400_apoyos_economicos.serializers import PagoApoyoSerializer
from ALC000_sistema_base.models.models import Usuario
from django.db.models import Q

# ViewSet para la gestión de pagos
class PagoApoyoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Pagos de Apoyos Económicos.
    """
    queryset = PagoApoyo.objects.all()
    serializer_class = PagoApoyoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Solo el usuario con email autorizado puede registrar pagos
        if self.request.user.email != "departamento.finanzas@conafe.com":
            return Response(
                {"error": "No tienes permiso para registrar pagos."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(registrado_por=self.request.user.email)


# API para registrar un nuevo pago
@permission_classes([IsAuthenticated])
class RegistrarPagoAPIView(APIView):
    """
    Endpoint para que el usuario autorizado registre pagos a otros usuarios (LEC).
    POST: /api/pagos/registrar/
    """
    def post(self, request):
        # Validar que el usuario autenticado sea el autorizado
        if request.user.email != "departamento.finanzas@conafe.com":
            return Response(
                {"error": "No tienes permiso para registrar pagos."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        try:
            # Validar que el usuario receptor existe
            usuario_receptor = Usuario.objects.get(id=data["usuario"])
        except Usuario.DoesNotExist:
            return Response(
                {"error": "El usuario receptor no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Crear el registro del pago
        serializer = PagoApoyoSerializer(data={
            "usuario": usuario_receptor.id,
            "concepto": data.get("concepto"),
            "monto": data.get("monto"),
            "estatus": data.get("estatus", "pendiente"),
            "registrado_por": request.user.email,
        })

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Pago registrado exitosamente.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API para listar pagos por usuario
@permission_classes([IsAuthenticated])
class ListarPagosPorUsuario(APIView):
    """
    Endpoint para obtener pagos de un usuario específico.
    GET: /api/pagos/usuario/<id>/
    """
    def get(self, request, usuario_id):
        try:
            pagos = PagoApoyo.objects.filter(usuario_id=usuario_id)
            serializer = PagoApoyoSerializer(pagos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Error al obtener pagos.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# API para listar pagos activos (pendientes de pago)
@permission_classes([AllowAny])
class PagosPendientesAPIView(APIView):
    """
    Endpoint para obtener la lista de pagos pendientes.
    GET: /api/pagos/pendientes/
    """
    def get(self, request):
        pagos_pendientes = PagoApoyo.objects.filter(estatus="pendiente")
        serializer = PagoApoyoSerializer(pagos_pendientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
