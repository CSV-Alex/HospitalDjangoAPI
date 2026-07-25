"""
Tests para la integración con Bonita usando mocks
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
from datetime import date, datetime
from apps.campana_vacunacion.domain.entities import (
    Campana, RegistroVacunacion, Vacuna, Lote
)
from apps.campana_vacunacion.domain.enums import (
    EstadoCampana, EstadoLote, EstadoRegistro, TipoVacuna
)
from apps.campana_vacunacion.interfaces.bonita_mocks import (
    BonitaMockClient, BonitaMockFactory, mock_bonita_request
)
from apps.campana_vacunacion.interfaces.bonita_service import (
    BonitaIntegrationService, BonitaCampaignWorkflow
)


class TestBonitaMockClient(unittest.TestCase):
    """Tests para el cliente mock de Bonita"""
    
    def setUp(self):
        """Configurar antes de cada test"""
        self.client = BonitaMockClient()
    
    def test_login_success(self):
        """Test: Login exitoso con credenciales correctas"""
        result = self.client.login('admin', 'admin')
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['data']['username'], 'admin')
        self.assertTrue(self.client.authenticated)
    
    def test_login_failure(self):
        """Test: Login fallido con credenciales incorrectas"""
        result = self.client.login('user', 'wrong_password')
        self.assertEqual(result['status_code'], 401)
        self.assertFalse(self.client.authenticated)
    
    def test_logout(self):
        """Test: Logout"""
        self.client.login('admin', 'admin')
        result = self.client.logout()
        self.assertEqual(result['status_code'], 200)
        self.assertFalse(self.client.authenticated)
    
    def test_get_processes(self):
        """Test: Obtener procesos disponibles"""
        self.client.login('admin', 'admin')
        result = self.client.get_processes()
        self.assertEqual(result['status_code'], 200)
        self.assertGreater(len(result['data']), 0)
        self.assertIn('hospital_campaign', 
                     [p['name'] for p in result['data']])
    
    def test_get_process_by_name(self):
        """Test: Obtener proceso por nombre"""
        self.client.login('admin', 'admin')
        result = self.client.get_process_by_name('hospital_campaign')
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['data']['name'], 'hospital_campaign')
    
    def test_start_process(self):
        """Test: Iniciar un proceso"""
        self.client.login('admin', 'admin')
        variables = {'campana_nombre': 'Test Campaign'}
        result = self.client.start_process('1', variables)
        self.assertEqual(result['status_code'], 201)
        self.assertIn('id', result['data'])
        self.assertEqual(result['data']['state'], 'INITIALIZING')
    
    def test_get_process_instances(self):
        """Test: Obtener instancias de proceso"""
        self.client.login('admin', 'admin')
        self.client.start_process('1')
        result = self.client.get_process_instances()
        self.assertEqual(result['status_code'], 200)
        self.assertGreater(len(result['data']), 0)
    
    def test_get_tasks(self):
        """Test: Obtener tareas"""
        self.client.login('admin', 'admin')
        result = self.client.get_tasks()
        self.assertEqual(result['status_code'], 200)
        self.assertGreater(len(result['data']), 0)
    
    def test_execute_task(self):
        """Test: Ejecutar/completar una tarea"""
        self.client.login('admin', 'admin')
        result = self.client.execute_task('mock_task_101')
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['data']['state'], 'COMPLETED')
    
    def test_set_process_variables(self):
        """Test: Establecer variables de proceso"""
        self.client.login('admin', 'admin')
        instance_id = self.client.start_process('1')['data']['id']
        variables = {'test_var': 'test_value'}
        result = self.client.set_process_variables(instance_id, variables)
        self.assertEqual(result['status_code'], 200)


class TestBonitaIntegrationService(unittest.TestCase):
    """Tests para el servicio de integración con Bonita"""
    
    def setUp(self):
        """Configurar antes de cada test"""
        self.service = BonitaIntegrationService(use_mock=True)
        self.service.authenticate()
    
    def test_authenticate(self):
        """Test: Autenticación con Bonita"""
        result = self.service.authenticate()
        self.assertTrue(result)
    
    def test_start_campaign_process(self):
        """Test: Iniciar proceso de campana"""
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test description',
            objetivo='Test objective',
            poblacion_objetivo='Población test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31),
            estado=EstadoCampana.PLANIF
        )
        
        result = self.service.start_campaign_process(campana)
        self.assertTrue(result['success'])
        self.assertIn('process_instance_id', result)
    
    def test_register_vaccination_in_bonita(self):
        """Test: Registrar vacunación en Bonita"""
        # Primero iniciar un proceso
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test',
            objetivo='Test',
            poblacion_objetivo='Test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        campaign_result = self.service.start_campaign_process(campana)
        process_id = campaign_result['process_instance_id']
        
        # Luego registrar una vacunación
        registro = RegistroVacunacion(
            campana_id=1,
            nombres='Juan',
            apellidos='Pérez',
            cedula='1234567890',
            edad=35,
            sexo='M',
            lote_id=1,
            sitio_vacunacion='Centro de Salud',
            personal_vacunador='Enfermera María',
            estado=EstadoRegistro.COMPLETO
        )
        
        result = self.service.register_vaccination_in_bonita(registro, process_id)
        self.assertTrue(result['success'])
    
    def test_get_campaign_tasks(self):
        """Test: Obtener tareas de campana"""
        # Primero iniciar un proceso
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test',
            objetivo='Test',
            poblacion_objetivo='Test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        campaign_result = self.service.start_campaign_process(campana)
        process_id = campaign_result['process_instance_id']
        
        # Obtener tareas
        tasks = self.service.get_campaign_tasks(process_id)
        self.assertGreater(len(tasks), 0)
        self.assertIn('id', tasks[0])
        self.assertIn('name', tasks[0])
    
    def test_get_available_processes(self):
        """Test: Obtener procesos disponibles"""
        processes = self.service.get_available_processes()
        self.assertGreater(len(processes), 0)
        process_names = [p['name'] for p in processes]
        self.assertIn('hospital_campaign', process_names)


class TestBonitaCampaignWorkflow(unittest.TestCase):
    """Tests para el flujo de trabajo de campanas"""
    
    def setUp(self):
        """Configurar antes de cada test"""
        self.workflow = BonitaCampaignWorkflow()
    
    def test_initialize_campaign(self):
        """Test: Inicializar campana completa"""
        campana = Campana(
            nombre='Campana Influenza 2026',
            descripcion='Vacunación contra influenza',
            objetivo='Vacunar 10000 personas',
            poblacion_objetivo='Mayor de 60 anos',
            vacuna_id=1,
            responsable='Dr. Juan Pérez',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        
        result = self.workflow.initialize_campaign(campana)
        self.assertTrue(result)
        self.assertIsNotNone(self.workflow.process_instance_id)
    
    def test_record_vaccination_in_workflow(self):
        """Test: Registrar vacunación en flujo"""
        # Inicializar campana
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test',
            objetivo='Test',
            poblacion_objetivo='Test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        self.workflow.initialize_campaign(campana)
        
        # Registrar vacunación
        registro = RegistroVacunacion(
            campana_id=1,
            nombres='Carlos',
            apellidos='García',
            cedula='9876543210',
            edad=45,
            sexo='M',
            lote_id=1,
            sitio_vacunacion='Clínica Central',
            personal_vacunador='Dr. Luis',
            estado=EstadoRegistro.COMPLETO
        )
        
        result = self.workflow.record_vaccination(registro)
        self.assertTrue(result)
    
    def test_get_pending_tasks_in_workflow(self):
        """Test: Obtener tareas pendientes en flujo"""
        # Inicializar campana
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test',
            objetivo='Test',
            poblacion_objetivo='Test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        self.workflow.initialize_campaign(campana)
        
        # Obtener tareas
        tasks = self.workflow.get_pending_tasks()
        self.assertGreater(len(tasks), 0)
    
    def test_get_campaign_status(self):
        """Test: Obtener estado de campana"""
        # Inicializar campana
        campana = Campana(
            nombre='Campana Test',
            descripcion='Test',
            objetivo='Test',
            poblacion_objetivo='Test',
            vacuna_id=1,
            responsable='Dr. Test',
            fecha_inicio=date(2026, 7, 21),
            fecha_fin=date(2026, 7, 31)
        )
        self.workflow.initialize_campaign(campana)
        
        # Obtener estado
        status = self.workflow.get_campaign_status()
        self.assertIsNotNone(status)


class TestMockBonitaRequest(unittest.TestCase):
    """Tests para el mock genérico de requests"""
    
    def test_mock_login_request(self):
        """Test: Mock de request de login"""
        response = mock_bonita_request('POST', 'http://localhost:8080/bonita/login')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('session_id', data)
    
    def test_mock_process_start_request(self):
        """Test: Mock de request para iniciar proceso"""
        response = mock_bonita_request('POST', 'http://localhost:8080/bonita/process/start')
        self.assertEqual(response.status_code, 201)
    
    def test_mock_task_request(self):
        """Test: Mock de request para obtener tareas"""
        response = mock_bonita_request('GET', 'http://localhost:8080/bonita/task')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
