import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..application.services import RegistrarConsultaService
from ..domain.exceptions import DomainException
from .serializers import (
    PacienteCreateSerializer,
    ConsultaResponseSerializer,
    PacienteListSerializer,
)
from ..models import Paciente as PacienteORM

logger = logging.getLogger(__name__)


class RegistrarConsultaView(APIView):
    """
    Recibe los datos del paciente, los valida aplicando DDD,
    los guarda en la base de datos y publica el resultado a RabbitMQa
    """
    
    @swagger_auto_schema(
        operation_id='registrar_consulta',
        operation_summary='Registrar una consulta médica',
        operation_description=(
            'Registra una nueva consulta desde Bonita '
            'Valida los datos del paciente, los guarda en BD '
            'y publica el resultado a RabbitMQ '
            'Este endpoint es usado por el Consumer de RabbitMQ de forma interna, '
            'pero también puede ser llamado directamente para testing'
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['numeroHistoriaClinica', 'nombreCompleto', 'fechaNacimiento', 'necesitaExamen'],
            properties={
                'numeroHistoriaClinica': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Número único de historia clínica',
                    example='HC-2026-001'
                ),
                'nombreCompleto': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Nombre completo del paciente',
                    example='Jose Garcia Perez'
                ),
                'fechaNacimiento': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='date',
                    description='Fecha de nacimiento (YYYY-MM-DD)',
                    example='1990-05-15'
                ),
                'necesitaExamen': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='El paciente necesita examen de laboratorio?',
                    example=True
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description='Consulta registrada exitosamente',
                schema=ConsultaResponseSerializer(),
                examples={
                    'application/json': {
                        'status': 'success',
                        'message': 'Consulta registrada exitosamente',
                        'necesita_examen': True,
                        'data': {
                            'numeroHistoriaClinica': 'HC-2026-001',
                            'nombreCompleto': 'Jose Garcia Perez'
                        }
                    }
                }
            ),
            400: openapi.Response(
                description='Datos inválidos (validación de negocio fallida)',
                examples={
                    'application/json': {
                        'status': 'error',
                        'message': 'Error de negocio: El número de historia clínica no puede estar vacío',
                        'type': 'domain_error'
                    }
                }
            ),
            500: openapi.Response(
                description='Error interno del servidor'
            ),
        },
        tags=['Consultas']
    )
    def post(self, request):
        try:
            logger.info(f"Request para registrar consulta: {request.data}")
            
            # Obtener datos del request
            datos = request.data
            
            # Validar que existan los campos requeridos
            campos_requeridos = [
                'numeroHistoriaClinica',
                'nombreCompleto',
                'fechaNacimiento',
                'necesitaExamen'
            ]
            
            campos_faltantes = [c for c in campos_requeridos if c not in datos]
            if campos_faltantes:
                return Response({
                    'status': 'error',
                    'message': f'Campos requeridos faltantes: {", ".join(campos_faltantes)}',
                    'type': 'validation_error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Registrar la consulta usando el Servicio de Aplicación
            service = RegistrarConsultaService()
            necesita_examen = service.registrar_consulta(datos)
            
            logger.info(f"Consulta registrada: necesita_examen = {necesita_examen}")
            
            return Response({
                'status': 'success',
                'message': 'Consulta registrada exitosamente',
                'necesita_examen': necesita_examen,
                'data': {
                    'numeroHistoriaClinica': datos.get('numeroHistoriaClinica'),
                    'nombreCompleto': datos.get('nombreCompleto'),
                }
            }, status=status.HTTP_201_CREATED)
        
        except DomainException as e:
            logger.error(f"Error de validación: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Error de negocio: {str(e)}',
                'type': 'domain_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': 'Error interno del servidor',
                'type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListarPacientesView(APIView):
    
    @swagger_auto_schema(
        operation_id='listar_pacientes',
        operation_summary='Listar todos los pacientes',
        operation_description='Obtiene un listado de todos los pacientes registrados en el sistema',
        responses={
            200: openapi.Response(
                description='Lista de pacientes obtenida exitosamente',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'numero_historia_clinica': openapi.Schema(type=openapi.TYPE_STRING),
                            'nombre_completo': openapi.Schema(type=openapi.TYPE_STRING),
                            'fecha_nacimiento': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                            'necesita_examen': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                ),
                examples={
                    'application/json': [
                        {
                            'numero_historia_clinica': 'HC-2026-001',
                            'nombre_completo': 'Jose Garcia Perez',
                            'fecha_nacimiento': '1990-05-15',
                            'necesita_examen': True,
                            'edad': 35
                        }
                    ]
                }
            ),
            500: openapi.Response(description='Error interno del servidor'),
        },
        tags=['Pacientes']
    )
    def get(self, request):
        """Listar todos los pacientes."""
        try:
            pacientes = PacienteORM.objects.all().values(
                'numero_historia_clinica',
                'nombre_completo',
                'fecha_nacimiento',
                'necesita_examen'
            )
            
            # Calcular edad para cada paciente
            from datetime import date
            pacientes_data = []
            for p in pacientes:
                edad = (date.today().year - p['fecha_nacimiento'].year)
                if (date.today().month, date.today().day) < (
                    p['fecha_nacimiento'].month, p['fecha_nacimiento'].day
                ):
                    edad -= 1
                
                pacientes_data.append({
                    **p,
                    'edad': edad
                })
            
            return Response(pacientes_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error al listar pacientes: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': 'Error al obtener pacientes',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObtenerPacienteView(APIView):
    """
    API para obtener detalles de un paciente específico.
    """
    
    @swagger_auto_schema(
        operation_id='obtener_paciente',
        operation_summary='Obtener detalles de un paciente',
        operation_description='Obtiene la información completa de un paciente específico por su número de historia clínica.',
        manual_parameters=[
            openapi.Parameter(
                name='numero_historia_clinica',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Número de historia clínica del paciente',
                example='HC-2026-001'
            ),
        ],
        responses={
            200: openapi.Response(
                description='Paciente encontrado',
                schema=PacienteListSerializer()
            ),
            404: openapi.Response(
                description='Paciente no encontrado'
            ),
            500: openapi.Response(
                description='Error interno del servidor'
            ),
        },
        tags=['Pacientes']
    )
    def get(self, request, numero_historia_clinica):
        try:
            paciente = PacienteORM.objects.get(
                numero_historia_clinica=numero_historia_clinica
            )
            
            # Calcular edad
            from datetime import date
            edad = (date.today().year - paciente.fecha_nacimiento.year)
            if (date.today().month, date.today().day) < (
                paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day
            ):
                edad -= 1
            
            return Response({
                'numero_historia_clinica': paciente.numero_historia_clinica,
                'nombre_completo': paciente.nombre_completo,
                'fecha_nacimiento': paciente.fecha_nacimiento,
                'necesita_examen': paciente.necesita_examen,
                'edad': edad,
            }, status=status.HTTP_200_OK)
        
        except PacienteORM.DoesNotExist:
            logger.warning(f"Paciente no encontrado: {numero_historia_clinica}")
            return Response({
                'status': 'error',
                'message': f'Paciente con número {numero_historia_clinica} no encontrado',
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error al obtener paciente: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': 'Error al obtener paciente',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)