"""
Servicio para integración con Bonita BPM
"""
from typing import Dict, Any, Optional, List
from apps.campana_vacunacion.interfaces.bonita_mocks import BonitaMockFactory, BonitaMockClient
from apps.campana_vacunacion.domain.entities import Campana, RegistroVacunacion


class BonitaIntegrationService:
    """Servicio para integrar procesos de campana de vacunación con Bonita BPM"""
    
    def __init__(self, use_mock: bool = True):
        """
        Inicializar el servicio de integración con Bonita
        
        Args:
            use_mock: Si True, usa mocks; si False, conecta con Bonita real
        """
        self.use_mock = use_mock
        if use_mock:
            self.client = BonitaMockFactory.get_client()
        else:
            # Aquí se crearía el cliente real de Bonita
            self.client = None
        
        self.campaign_process_id = '1'
        self.vaccine_registration_process_id = '2'
    
    def authenticate(self, username: str = 'admin', password: str = 'admin') -> bool:
        """Autenticarse con Bonita"""
        response = self.client.login(username, password)
        return response['status_code'] == 200
    
    def start_campaign_process(self, campana: Campana) -> Dict[str, Any]:
        """Iniciar un proceso de campana en Bonita"""
        variables = {
            'campana_nombre': campana.nombre,
            'campana_descripcion': campana.descripcion,
            'campana_objetivo': campana.objetivo,
            'poblacion_objetivo': campana.poblacion_objetivo,
            'vacuna_id': campana.vacuna_id,
            'responsable': campana.responsable,
            'fecha_inicio': str(campana.fecha_inicio),
            'fecha_fin': str(campana.fecha_fin),
            'estado': campana.estado.value
        }
        
        response = self.client.start_process(self.campaign_process_id, variables)
        
        if response['status_code'] == 201:
            return {
                'success': True,
                'process_instance_id': response['data']['id'],
                'message': f'Campana "{campana.nombre}" iniciada en Bonita'
            }
        else:
            return {
                'success': False,
                'error': response['data'].get('error', 'Error desconocido')
            }
    
    def register_vaccination_in_bonita(self, registro: RegistroVacunacion, 
                                       process_instance_id: str) -> Dict[str, Any]:
        """Registrar una vacunación en el proceso de Bonita"""
        variables = {
            'persona_nombres': registro.nombres,
            'persona_apellidos': registro.apellidos,
            'persona_cedula': registro.cedula,
            'persona_edad': registro.edad,
            'persona_sexo': registro.sexo,
            'lote_id': registro.lote_id,
            'sitio_vacunacion': registro.sitio_vacunacion,
            'personal_vacunador': registro.personal_vacunador,
            'fecha_vacunacion': str(registro.fecha_vacunacion),
            'observaciones': registro.observaciones or ''
        }
        
        response = self.client.set_process_variables(process_instance_id, variables)
        
        if response['status_code'] == 200:
            return {
                'success': True,
                'message': f'Vacunación de {registro.nombres} registrada en Bonita'
            }
        else:
            return {
                'success': False,
                'error': response['data'].get('error', 'Error desconocido')
            }
    
    def get_campaign_tasks(self, process_instance_id: str) -> List[Dict[str, Any]]:
        """Obtener las tareas pendientes de una campana"""
        response = self.client.get_tasks(process_instance_id)
        
        if response['status_code'] == 200:
            return response['data']
        else:
            return []
    
    def approve_campaign_review(self, process_instance_id: str, task_id: str,
                                approval_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Aprobar la revisión de campana"""
        variables = approval_data or {
            'revision_aprobada': True,
            'comentarios': 'Campana aprobada'
        }
        
        response = self.client.execute_task(task_id, variables)
        
        if response['status_code'] == 200:
            return {
                'success': True,
                'message': 'Revisión de campana aprobada',
                'task_id': task_id
            }
        else:
            return {
                'success': False,
                'error': response['data'].get('error', 'Error desconocido')
            }
    
    def get_process_instances(self) -> List[Dict[str, Any]]:
        """Obtener todas las instancias de proceso"""
        response = self.client.get_process_instances()
        
        if response['status_code'] == 200:
            return response['data']
        else:
            return []
    
    def get_process_variables(self, process_instance_id: str) -> Dict[str, Any]:
        """Obtener las variables de un proceso"""
        response = self.client.get_process_variables(process_instance_id)
        
        if response['status_code'] == 200:
            return response['data']
        else:
            return {}
    
    def get_available_processes(self) -> List[Dict[str, Any]]:
        """Obtener procesos disponibles en Bonita"""
        response = self.client.get_processes()
        
        if response['status_code'] == 200:
            return response['data']
        else:
            return []
    
    def disconnect(self):
        """Desconectar de Bonita"""
        return self.client.logout()


class BonitaCampaignWorkflow:
    """Flujo de trabajo completo para campanas de vacunación en Bonita"""
    
    def __init__(self):
        self.bonita_service = BonitaIntegrationService(use_mock=True)
        self.process_instance_id = None
    
    def initialize_campaign(self, campana: Campana) -> bool:
        """Inicializar un flujo de campana completo"""
        # Autenticar
        if not self.bonita_service.authenticate():
            print("Error: No se pudo autenticar con Bonita")
            return False
        
        # Iniciar proceso
        result = self.bonita_service.start_campaign_process(campana)
        if not result['success']:
            print(f"Error: {result['error']}")
            return False
        
        self.process_instance_id = result['process_instance_id']
        print(f"✓ Proceso iniciado: {self.process_instance_id}")
        return True
    
    def record_vaccination(self, registro: RegistroVacunacion) -> bool:
        """Registrar una vacunación en el flujo"""
        if not self.process_instance_id:
            print("Error: No hay un proceso iniciado")
            return False
        
        result = self.bonita_service.register_vaccination_in_bonita(
            registro, 
            self.process_instance_id
        )
        
        if not result['success']:
            print(f"Error: {result['error']}")
            return False
        
        print(f"✓ Vacunación registrada: {result['message']}")
        return True
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Obtener tareas pendientes del flujo"""
        if not self.process_instance_id:
            return []
        
        return self.bonita_service.get_campaign_tasks(self.process_instance_id)
    
    def complete_task(self, task_id: str, approval_data: Dict[str, Any] = None) -> bool:
        """Completar una tarea del flujo"""
        if not self.process_instance_id:
            print("Error: No hay un proceso iniciado")
            return False
        
        result = self.bonita_service.approve_campaign_review(
            self.process_instance_id,
            task_id,
            approval_data
        )
        
        if not result['success']:
            print(f"Error: {result['error']}")
            return False
        
        print(f"✓ Tarea completada: {result['message']}")
        return True
    
    def get_campaign_status(self) -> Dict[str, Any]:
        """Obtener el estado actual de la campana"""
        if not self.process_instance_id:
            return {}
        
        return self.bonita_service.get_process_variables(self.process_instance_id)
    
    def finalize(self):
        """Finalizar el flujo y desconectar"""
        self.bonita_service.disconnect()
        print("✓ Desconectado de Bonita")
