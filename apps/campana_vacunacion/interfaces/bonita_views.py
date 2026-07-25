"""
Controladores (Views) integrados con Bonita BPM
Reemplazan los endpoints mock básicos con flujos reales de Bonita
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from apps.campana_vacunacion.domain.entities import (
    Campana, RegistroVacunacion
)
from apps.campana_vacunacion.domain.enums import EstadoCampana, EstadoRegistro
from apps.campana_vacunacion.interfaces.bonita_service import (
    BonitaIntegrationService, BonitaCampaignWorkflow
)


# Servicio global de Bonita (singleton)
_bonita_service = None
_bonita_workflow = None

def get_bonita_service(use_mock: bool = True):
    """Obtener instancia del servicio de Bonita"""
    global _bonita_service
    if _bonita_service is None:
        _bonita_service = BonitaIntegrationService(use_mock=use_mock)
    return _bonita_service

def get_bonita_workflow(use_mock: bool = True):
    """Obtener instancia del flujo de trabajo de Bonita"""
    global _bonita_workflow
    if _bonita_workflow is None:
        _bonita_workflow = BonitaCampaignWorkflow()
    return _bonita_workflow


# ============================================================================
# ENDPOINTS PARA CAMPAnA (CON INTEGRACIÓN A BONITA)
# ============================================================================

@api_view(['POST'])
def crear_campana_con_bonita(request):
    """
    Crear una campana e iniciar su proceso en Bonita
    
    POST /api/vacunacion/campanas/bonita/crear/
    Body:
    {
        "nombre": "Campana Influenza 2026",
        "descripcion": "Vacunación contra influenza",
        "objetivo": "Vacunar 10000 personas",
        "poblacion_objetivo": "Mayor de 60 anos",
        "vacuna_id": 1,
        "responsable": "Dr. Juan Pérez",
        "fecha_inicio": "2026-07-21",
        "fecha_fin": "2026-07-31"
    }
    """
    try:
        service = get_bonita_service(use_mock=True)
        
        # Autenticar con Bonita
        if not service.authenticate():
            return Response(
                {'error': 'No se pudo autenticar con Bonita'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Crear entidad de campana
        campana = Campana(
            nombre=request.data.get('nombre'),
            descripcion=request.data.get('descripcion'),
            objetivo=request.data.get('objetivo'),
            poblacion_objetivo=request.data.get('poblacion_objetivo'),
            vacuna_id=request.data.get('vacuna_id'),
            responsable=request.data.get('responsable'),
            fecha_inicio=request.data.get('fecha_inicio'),
            fecha_fin=request.data.get('fecha_fin'),
            estado=EstadoCampana.PLANIF
        )
        
        # Iniciar proceso en Bonita
        result = service.start_campaign_process(campana)
        
        if result['success']:
            return Response({
                'id': 1,  # Aquí iría el ID de BD
                'nombre': campana.nombre,
                'bonita_process_id': result['process_instance_id'],
                'estado': EstadoCampana.PLANIF.value,
                'mensaje': result['message']
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Error al crear campana: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def obtener_campana_con_bonita(request, campana_id, bonita_instance_id):
    """
    Obtener campana y su estado en Bonita
    
    GET /api/vacunacion/campanas/bonita/{campana_id}/{bonita_instance_id}/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        # Obtener variables del proceso en Bonita
        variables = service.get_process_variables(bonita_instance_id)
        
        # Obtener tareas pendientes
        tasks = service.get_campaign_tasks(bonita_instance_id)
        
        return Response({
            'id': campana_id,
            'nombre': variables.get('campana_nombre', 'N/A'),
            'objetivo': variables.get('campana_objetivo', 'N/A'),
            'estado': variables.get('estado', 'N/A'),
            'bonita_instance_id': bonita_instance_id,
            'variables': variables,
            'tareas_pendientes': [
                {'id': t['id'], 'nombre': t['displayName'], 'estado': t['state']}
                for t in tasks
            ]
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================================
# ENDPOINTS PARA REGISTROS DE VACUNACIÓN (CON INTEGRACIÓN A BONITA)
# ============================================================================

@api_view(['POST'])
def registrar_vacunacion_con_bonita(request):
    """
    Registrar vacunación e integrar con Bonita
    
    POST /api/vacunacion/registros/bonita/crear/
    Body:
    {
        "campana_id": 1,
        "bonita_instance_id": "mock_process_instance_789",
        "nombres": "Juan",
        "apellidos": "García",
        "cedula": "1234567890",
        "edad": 72,
        "sexo": "M",
        "lote_id": 1,
        "sitio_vacunacion": "Centro de Salud",
        "personal_vacunador": "Enfermera Rosa",
        "observaciones": "Sin reacciones"
    }
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        bonita_instance_id = request.data.get('bonita_instance_id')
        
        # Crear registro de vacunación
        registro = RegistroVacunacion(
            campana_id=request.data.get('campana_id'),
            nombres=request.data.get('nombres'),
            apellidos=request.data.get('apellidos'),
            cedula=request.data.get('cedula'),
            edad=request.data.get('edad', 0),
            sexo=request.data.get('sexo'),
            lote_id=request.data.get('lote_id'),
            sitio_vacunacion=request.data.get('sitio_vacunacion'),
            personal_vacunador=request.data.get('personal_vacunador'),
            observaciones=request.data.get('observaciones', ''),
            estado=EstadoRegistro.COMPLETO
        )
        
        # Registrar en Bonita
        result = service.register_vaccination_in_bonita(registro, bonita_instance_id)
        
        if result['success']:
            return Response({
                'id': 1,  # Aquí iría el ID de BD
                'cedula': registro.cedula,
                'nombres': registro.nombres,
                'apellidos': registro.apellidos,
                'bonita_status': 'registrado',
                'mensaje': result['message']
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Error al registrar vacunación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def listar_registros_por_campana_con_bonita(request, campana_id, bonita_instance_id):
    """
    Listar registros de vacunación de una campana desde Bonita
    
    GET /api/vacunacion/registros/bonita/campana/{campana_id}/{bonita_instance_id}/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        # Obtener variables del proceso (incluyen registros)
        variables = service.get_process_variables(bonita_instance_id)
        
        # Construir lista de registros desde las variables
        registros = []
        for i in range(1, 10):  # Asumir máximo 10 registros
            if f'persona_nombres_{i}' in variables:
                registros.append({
                    'nombres': variables.get(f'persona_nombres_{i}'),
                    'apellidos': variables.get(f'persona_apellidos_{i}'),
                    'cedula': variables.get(f'persona_cedula_{i}'),
                    'fecha_vacunacion': variables.get(f'fecha_vacunacion_{i}')
                })
        
        return Response({
            'campana_id': campana_id,
            'bonita_instance_id': bonita_instance_id,
            'total_registros': len(registros),
            'registros': registros
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================================
# ENDPOINTS PARA TAREAS DE BONITA
# ============================================================================

@api_view(['GET'])
def obtener_tareas_campana(request, bonita_instance_id):
    """
    Obtener tareas pendientes de una campana en Bonita
    
    GET /api/vacunacion/bonita/tareas/{bonita_instance_id}/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        tasks = service.get_campaign_tasks(bonita_instance_id)
        
        return Response({
            'bonita_instance_id': bonita_instance_id,
            'total_tareas': len(tasks),
            'tareas': [
                {
                    'id': t['id'],
                    'nombre': t['displayName'],
                    'estado': t['state'],
                    'prioridad': t.get('priority'),
                    'fecha_vencimiento': t.get('dueDate')
                }
                for t in tasks
            ]
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def completar_tarea_campana(request, bonita_instance_id, task_id):
    """
    Completar una tarea de campana en Bonita
    
    POST /api/vacunacion/bonita/tareas/{bonita_instance_id}/{task_id}/completar/
    Body:
    {
        "revision_aprobada": true,
        "comentarios": "Campana aprobada para ejecución"
    }
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        approval_data = {
            'revision_aprobada': request.data.get('revision_aprobada', True),
            'comentarios': request.data.get('comentarios', '')
        }
        
        result = service.approve_campaign_review(
            bonita_instance_id,
            task_id,
            approval_data
        )
        
        if result['success']:
            return Response({
                'task_id': result['task_id'],
                'estado': 'completada',
                'mensaje': result['message']
            })
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================================
# ENDPOINTS PARA FLUJO COMPLETO
# ============================================================================

@api_view(['POST'])
def inicializar_flujo_campana(request):
    """
    Inicializar un flujo completo de campana
    
    POST /api/vacunacion/bonita/flujo/inicializar/
    Body:
    {
        "nombre": "Campana Influenza 2026",
        "descripcion": "Vacunación contra influenza",
        "objetivo": "Vacunar 10000 personas",
        "poblacion_objetivo": "Mayor de 60 anos",
        "vacuna_id": 1,
        "responsable": "Dr. Juan Pérez",
        "fecha_inicio": "2026-07-21",
        "fecha_fin": "2026-07-31"
    }
    """
    try:
        workflow = get_bonita_workflow(use_mock=True)
        
        # Crear campana
        campana = Campana(
            nombre=request.data.get('nombre'),
            descripcion=request.data.get('descripcion'),
            objetivo=request.data.get('objetivo'),
            poblacion_objetivo=request.data.get('poblacion_objetivo'),
            vacuna_id=request.data.get('vacuna_id'),
            responsable=request.data.get('responsable'),
            fecha_inicio=request.data.get('fecha_inicio'),
            fecha_fin=request.data.get('fecha_fin'),
            estado=EstadoCampana.PLANIF
        )
        
        # Inicializar flujo
        if workflow.initialize_campaign(campana):
            return Response({
                'success': True,
                'process_instance_id': workflow.process_instance_id,
                'nombre': campana.nombre,
                'estado': EstadoCampana.PLANIF.value,
                'mensaje': 'Flujo de campana inicializado en Bonita'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'No se pudo inicializar el flujo'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def obtener_estado_flujo(request, bonita_instance_id):
    """
    Obtener estado actual del flujo de campana
    
    GET /api/vacunacion/bonita/flujo/{bonita_instance_id}/estado/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        # Obtener variables y tareas
        variables = service.get_process_variables(bonita_instance_id)
        tasks = service.get_campaign_tasks(bonita_instance_id)
        
        return Response({
            'bonita_instance_id': bonita_instance_id,
            'estado': variables.get('estado', 'N/A'),
            'campana_nombre': variables.get('campana_nombre', 'N/A'),
            'campana_objetivo': variables.get('campana_objetivo', 'N/A'),
            'responsable': variables.get('responsable', 'N/A'),
            'tareas_pendientes': len([t for t in tasks if t['state'] == 'READY']),
            'total_tareas': len(tasks),
            'variables': variables,
            'tareas': [
                {
                    'id': t['id'],
                    'nombre': t['displayName'],
                    'estado': t['state']
                }
                for t in tasks
            ]
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================================================
# ENDPOINTS DE UTILIDAD
# ============================================================================

@api_view(['GET'])
def listar_procesos_disponibles(request):
    """
    Listar procesos disponibles en Bonita
    
    GET /api/vacunacion/bonita/procesos/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        processes = service.get_available_processes()
        
        return Response({
            'total_procesos': len(processes),
            'procesos': [
                {
                    'id': p['id'],
                    'nombre': p['displayName'],
                    'nombre_tecnico': p['name'],
                    'version': p['version'],
                    'estado': p['state']
                }
                for p in processes
            ]
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def listar_instancias_proceso(request):
    """
    Listar todas las instancias de proceso
    
    GET /api/vacunacion/bonita/instancias/
    """
    try:
        service = get_bonita_service(use_mock=True)
        service.authenticate()
        
        instances = service.get_process_instances()
        
        return Response({
            'total_instancias': len(instances),
            'instancias': instances
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
