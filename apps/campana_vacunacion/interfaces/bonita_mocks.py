"""
Mocks para emular conexiones con Bonita BPM
"""
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, Optional, List
import json


class BonitaMockClient:
    """Mock del cliente HTTP para Bonita"""
    
    def __init__(self, base_url: str = 'http://localhost:8080/bonita'):
        self.base_url = base_url
        self.session_id = None
        self.authenticated = False
        self.processes = {}
        self.process_instances = {}
        self.tasks = {}
        self.variables = {}
        
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Mock de login a Bonita"""
        if username == 'admin' and password == 'admin':
            self.session_id = 'mock_session_12345'
            self.authenticated = True
            return {
                'status_code': 200,
                'data': {
                    'session_id': self.session_id,
                    'username': username,
                    'user_id': 1
                }
            }
        else:
            return {
                'status_code': 401,
                'data': {'error': 'Invalid credentials'}
            }
    
    def logout(self) -> Dict[str, Any]:
        """Mock de logout de Bonita"""
        self.authenticated = False
        self.session_id = None
        return {
            'status_code': 200,
            'data': {'message': 'Logged out successfully'}
        }
    
    def get_processes(self) -> Dict[str, Any]:
        """Mock para obtener procesos disponibles en Bonita"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        return {
            'status_code': 200,
            'data': [
                {
                    'id': '1',
                    'name': 'hospital_campaign',
                    'displayName': 'Hospital Campaign Process',
                    'version': '1.0',
                    'state': 'ENABLED'
                },
                {
                    'id': '2',
                    'name': 'vaccine_registration',
                    'displayName': 'Vaccine Registration Process',
                    'version': '1.0',
                    'state': 'ENABLED'
                }
            ]
        }
    
    def get_process_by_name(self, process_name: str) -> Dict[str, Any]:
        """Mock para obtener un proceso por nombre"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        processes = {
            'hospital_campaign': {'id': '1', 'name': 'hospital_campaign', 'version': '1.0'},
            'vaccine_registration': {'id': '2', 'name': 'vaccine_registration', 'version': '1.0'}
        }
        
        if process_name in processes:
            return {
                'status_code': 200,
                'data': processes[process_name]
            }
        else:
            return {
                'status_code': 404,
                'data': {'error': f'Process {process_name} not found'}
            }
    
    def start_process(self, process_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock para iniciar un proceso"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        instance_id = f'mock_process_instance_{len(self.process_instances) + 789}'
        self.process_instances[instance_id] = {
            'id': instance_id,
            'processDefinitionId': process_id,
            'state': 'INITIALIZING',
            'variables': variables or {}
        }
        
        return {
            'status_code': 201,
            'data': {
                'id': instance_id,
                'processDefinitionId': process_id,
                'state': 'INITIALIZING',
                'startDate': '2026-07-21T10:30:00.000Z',
                'variables': variables or {}
            }
        }
    
    def get_process_instances(self, process_id: str = None) -> Dict[str, Any]:
        """Mock para obtener instancias de proceso"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        instances = list(self.process_instances.values())
        if process_id:
            instances = [i for i in instances if i['processDefinitionId'] == process_id]
        
        return {
            'status_code': 200,
            'data': instances
        }
    
    def get_process_instance(self, instance_id: str) -> Dict[str, Any]:
        """Mock para obtener una instancia específica"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        if instance_id in self.process_instances:
            return {
                'status_code': 200,
                'data': self.process_instances[instance_id]
            }
        else:
            return {
                'status_code': 404,
                'data': {'error': f'Instance {instance_id} not found'}
            }
    
    def get_tasks(self, process_instance_id: str = None, state: str = None) -> Dict[str, Any]:
        """Mock para obtener tareas"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        tasks = [
            {
                'id': 'mock_task_101',
                'name': 'Review Campaign',
                'displayName': 'Review Campaign Configuration',
                'processInstanceId': process_instance_id or 'mock_process_instance_789',
                'state': 'READY',
                'priority': '1',
                'dueDate': '2026-07-22T10:00:00.000Z'
            },
            {
                'id': 'mock_task_102',
                'name': 'Approve Campaign',
                'displayName': 'Approve Campaign Deployment',
                'processInstanceId': process_instance_id or 'mock_process_instance_789',
                'state': 'READY',
                'priority': '2',
                'dueDate': '2026-07-23T10:00:00.000Z'
            }
        ]
        
        if process_instance_id:
            tasks = [t for t in tasks if t['processInstanceId'] == process_instance_id]
        
        if state:
            tasks = [t for t in tasks if t['state'] == state]
        
        return {
            'status_code': 200,
            'data': tasks
        }
    
    def execute_task(self, task_id: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock para ejecutar/completar una tarea"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        return {
            'status_code': 200,
            'data': {
                'id': task_id,
                'state': 'COMPLETED',
                'completedDate': '2026-07-21T11:30:00.000Z',
                'variables': variables or {}
            }
        }
    
    def get_process_variables(self, process_instance_id: str) -> Dict[str, Any]:
        """Mock para obtener variables de un proceso"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        if process_instance_id in self.process_instances:
            return {
                'status_code': 200,
                'data': self.process_instances[process_instance_id].get('variables', {})
            }
        else:
            return {
                'status_code': 404,
                'data': {'error': f'Instance {process_instance_id} not found'}
            }
    
    def set_process_variables(self, process_instance_id: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Mock para establecer variables de un proceso"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        if process_instance_id in self.process_instances:
            self.process_instances[process_instance_id]['variables'].update(variables)
            return {
                'status_code': 200,
                'data': {
                    'message': 'Variables updated successfully',
                    'variables': self.process_instances[process_instance_id]['variables']
                }
            }
        else:
            return {
                'status_code': 404,
                'data': {'error': f'Instance {process_instance_id} not found'}
            }
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Mock para obtener una tarea específica"""
        if not self.authenticated:
            return {
                'status_code': 401,
                'data': {'error': 'Not authenticated'}
            }
        
        tasks = {
            'mock_task_101': {
                'id': 'mock_task_101',
                'name': 'Review Campaign',
                'state': 'READY'
            },
            'mock_task_102': {
                'id': 'mock_task_102',
                'name': 'Approve Campaign',
                'state': 'READY'
            }
        }
        
        if task_id in tasks:
            return {
                'status_code': 200,
                'data': tasks[task_id]
            }
        else:
            return {
                'status_code': 404,
                'data': {'error': f'Task {task_id} not found'}
            }


class BonitaMockFactory:
    """Factory para crear mocks de Bonita"""
    
    _instance = None
    
    @classmethod
    def get_client(cls, base_url: str = 'http://localhost:8080/bonita') -> BonitaMockClient:
        """Obtener instancia singleton del cliente mock"""
        if cls._instance is None:
            cls._instance = BonitaMockClient(base_url)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Resetear la instancia para tests"""
        cls._instance = None


def mock_bonita_request(method: str, url: str, **kwargs) -> Mock:
    """Mock genérico para requests HTTP a Bonita"""
    response = Mock()
    
    if 'login' in url:
        response.status_code = 200
        response.json.return_value = {'session_id': 'mock_session_12345'}
    elif 'process' in url and 'start' in url:
        response.status_code = 201
        response.json.return_value = {'id': 'mock_instance_789', 'state': 'INITIALIZING'}
    elif 'process' in url:
        response.status_code = 200
        response.json.return_value = [{'id': '1', 'name': 'hospital_campaign'}]
    elif 'task' in url:
        response.status_code = 200
        response.json.return_value = [{'id': 'task_1', 'name': 'Review', 'state': 'READY'}]
    else:
        response.status_code = 404
        response.json.return_value = {'error': 'Not found'}
    
    return response
