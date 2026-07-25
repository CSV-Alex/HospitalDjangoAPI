"""
Configuración de Bonita para desarrollo y testing
"""

# Configuración de Bonita
BONITA_CONFIG = {
    'BASE_URL': 'http://localhost:8080/bonita',
    'API_VERSION': 'bpm',
    'USERNAME': 'admin',
    'PASSWORD': 'admin',
    'TENANT_ID': '1',
    'PROCESS_NAME': 'hospital_campaign',
}

# Respuestas simuladas de Bonita
BONITA_MOCK_RESPONSES = {
    'login': {
        'status_code': 200,
        'data': {
            'session_id': 'mock_session_12345',
            'username': 'admin',
            'user_id': 1
        }
    },
    'get_processes': {
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
    },
    'start_process': {
        'status_code': 201,
        'data': {
            'id': 'mock_process_instance_789',
            'processDefinitionId': '1',
            'state': 'INITIALIZING',
            'startDate': '2026-07-21T10:30:00.000Z'
        }
    },
    'get_process_instances': {
        'status_code': 200,
        'data': [
            {
                'id': 'mock_process_instance_789',
                'processDefinitionId': '1',
                'processDefinitionName': 'hospital_campaign',
                'state': 'COMPLETED',
                'startDate': '2026-07-21T10:30:00.000Z',
                'endDate': '2026-07-21T11:00:00.000Z'
            }
        ]
    },
    'get_tasks': {
        'status_code': 200,
        'data': [
            {
                'id': 'mock_task_101',
                'name': 'Review Campaign',
                'displayName': 'Review Campaign Configuration',
                'processInstanceId': 'mock_process_instance_789',
                'state': 'READY',
                'priority': '1',
                'dueDate': '2026-07-22T10:00:00.000Z'
            },
            {
                'id': 'mock_task_102',
                'name': 'Approve Campaign',
                'displayName': 'Approve Campaign Deployment',
                'processInstanceId': 'mock_process_instance_789',
                'state': 'READY',
                'priority': '2',
                'dueDate': '2026-07-23T10:00:00.000Z'
            }
        ]
    },
    'execute_task': {
        'status_code': 200,
        'data': {
            'id': 'mock_task_101',
            'state': 'COMPLETED',
            'completedDate': '2026-07-21T11:30:00.000Z'
        }
    },
    'get_process_variables': {
        'status_code': 200,
        'data': {
            'campana_nombre': 'Campana Influenza 2026',
            'campana_objetivo': 'Vacunar 10000 personas',
            'vacuna_tipo': 'ARN',
            'responsable': 'Dr. Juan Pérez',
            'estado': 'EN_CURSO'
        }
    },
    'error_unauthorized': {
        'status_code': 401,
        'data': {
            'error': 'Invalid credentials',
            'message': 'Authentication failed'
        }
    },
    'error_not_found': {
        'status_code': 404,
        'data': {
            'error': 'Resource not found',
            'message': 'The requested resource does not exist'
        }
    }
}
