from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
try:
    from drf_yasg.utils import swagger_auto_schema
except ImportError:
    # Fallback if drf-yasg is not installed
    def swagger_auto_schema(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

from ..services import AdmisionService
from ..application.services import ProcesarHospitalizacionService
from .serializers import (
    RecepcionOrdenSerializer,
    ValidarCoberturaSerializer,
    IniciarHospitalizacionSerializer,
    OrdenInternamientoSerializer,
    HospitalizacionSerializer,
    HospitalizacionRequestSerializer
)
from ..models import OrdenInternamiento, Hospitalizacion

@swagger_auto_schema(
    method='post',
    request_body=HospitalizacionRequestSerializer,
    responses={201: 'Hospitalización registrada', 400: 'Error de validación', 500: 'Error interno'}
)
@api_view(['POST'])
def procesar_solicitud_hospitalizacion_api(request):
    """
    Endpoint para procesar solicitudes de hospitalización (Alternativa REST al RabbitMQ).
    """
    serializer = HospitalizacionRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        servicio = ProcesarHospitalizacionService()
        servicio.procesar_solicitud(serializer.validated_data)
        return Response({'mensaje': 'Hospitalización procesada exitosamente'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def recepcionar_orden(request):
    serializer = RecepcionOrdenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        orden = AdmisionService.recepcionar_orden(serializer.validated_data)
        return Response({
            'mensaje': 'Orden recepcionada correctamente',
            'orden_id': orden.id,
            'estado': orden.estado
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def verificar_disponibilidad(request, orden_id):
    try:
        resultado = AdmisionService.verificar_disponibilidad(orden_id)
        return Response(resultado, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def validar_cobertura(request, orden_id):
    serializer = ValidarCoberturaSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = AdmisionService.validar_cobertura_sis(orden_id, serializer.validated_data['codigo_sis'])
        return Response(resultado, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def iniciar_hospitalizacion(request, orden_id):
    serializer = IniciarHospitalizacionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = AdmisionService.iniciar_hospitalizacion(
            orden_id,
            serializer.validated_data['signos_vitales']
        )
        return Response(resultado, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def listar_ordenes(request):
    ordenes = OrdenInternamiento.objects.all()
    serializer = OrdenInternamientoSerializer(ordenes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_hospitalizacion(request, hospitalizacion_id):
    try:
        hosp = Hospitalizacion.objects.get(id=hospitalizacion_id)
        serializer = HospitalizacionSerializer(hosp)
        return Response(serializer.data)
    except Hospitalizacion.DoesNotExist:
        return Response({'error': 'Hospitalización no encontrada'}, status=status.HTTP_404_NOT_FOUND)
