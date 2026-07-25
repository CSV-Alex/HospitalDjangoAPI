"""
Ejemplos de uso de los mocks de Bonita
"""
from datetime import date
from apps.campana_vacunacion.domain.entities import (
    Campana, RegistroVacunacion, Vacuna, Lote
)
from apps.campana_vacunacion.domain.enums import (
    EstadoCampana, EstadoLote, EstadoRegistro, TipoVacuna
)
from apps.campana_vacunacion.interfaces.bonita_mocks import BonitaMockClient, BonitaMockFactory
from apps.campana_vacunacion.interfaces.bonita_service import (
    BonitaIntegrationService, BonitaCampaignWorkflow
)


def ejemplo_1_cliente_basico(): 
    print("\n" + "="*60)
    print("EJEMPLO 1: Cliente Básico de Bonita")
    print("="*60)
    
    # Crear cliente
    client = BonitaMockClient()
    
    # Autenticarse
    login_result = client.login('admin', 'admin')
    print(f"✓ Login: {login_result['data']['username']}")
    
    # Obtener procesos disponibles
    processes = client.get_processes()
    print(f"✓ Procesos disponibles:")
    for process in processes['data']:
        print(f"  - {process['displayName']} (ID: {process['id']})")
    
    # Logout
    logout_result = client.logout()
    print(f"✓ Logout realizado")


def ejemplo_2_iniciar_proceso():
    """
    Ejemplo 2: Iniciar un proceso de campana en Bonita
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: Iniciar Proceso de Campana")
    print("="*60)
    
    client = BonitaMockClient()
    client.login('admin', 'admin')
    
    # Definir variables de la campana
    variables = {
        'campana_nombre': 'Campana Influenza 2026',
        'campana_objetivo': 'Vacunar 10,000 personas',
        'vacuna_tipo': 'ARN',
        'responsable': 'Dr. Juan Pérez',
        'estado': 'EN_CURSO'
    }
    
    # Iniciar proceso
    result = client.start_process('1', variables)
    
    print(f"✓ Proceso iniciado")
    print(f"  ID de instancia: {result['data']['id']}")
    print(f"  Estado: {result['data']['state']}")
    print(f"  Fecha inicio: {result['data']['startDate']}")
    
    # Obtener instancias creadas
    instances = client.get_process_instances()
    print(f"✓ Instancias en el sistema: {len(instances['data'])}")


def ejemplo_3_servicio_integracion():
    """
    Ejemplo 3: Usar el servicio de integración
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: Servicio de Integración")
    print("="*60)
    
    # Crear servicio
    service = BonitaIntegrationService(use_mock=True)
    
    # Autenticarse
    is_auth = service.authenticate()
    print(f"✓ Autenticado: {is_auth}")
    
    # Crear una campana
    campana = Campana(
        nombre='Campana de Vacunación COVID-19',
        descripcion='Tercera dosis de refuerzo',
        objetivo='Vacunar 5,000 personas',
        poblacion_objetivo='Mayor de 70 anos',
        vacuna_id=1,
        responsable='Dra. María Rodríguez',
        fecha_inicio=date(2026, 7, 21),
        fecha_fin=date(2026, 7, 31),
        estado=EstadoCampana.EN_CURSO
    )
    
    # Iniciar la campana en Bonita
    result = service.start_campaign_process(campana)
    if result['success']:
        process_id = result['process_instance_id']
        print(f"✓ {result['message']}")
        print(f"  ID de proceso: {process_id}")
        
        # Obtener variables del proceso
        variables = service.get_process_variables(process_id)
        print(f"✓ Variables del proceso:")
        for key, value in variables.items():
            print(f"  - {key}: {value}")
    else:
        print(f"✗ Error: {result['error']}")


def ejemplo_4_flujo_completo():
    """
    Ejemplo 4: Flujo completo de campana de vacunación
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: Flujo Completo de Campana")
    print("="*60)
    
    # Crear flujo de trabajo
    workflow = BonitaCampaignWorkflow()
    
    # Crear campana
    campana = Campana(
        nombre='Campana de Vacunación - Temporada 2026',
        descripcion='Vacunación para influenza, neumonía y COVID-19',
        objetivo='Alcanzar 80% de cobertura en población vulnerable',
        poblacion_objetivo='Adultos mayores (60+) y trabajadores de salud',
        vacuna_id=1,
        responsable='Dr. Carlos López',
        fecha_inicio=date(2026, 8, 1),
        fecha_fin=date(2026, 12, 31),
        estado=EstadoCampana.PLANIF
    )
    
    # Inicializar campana en Bonita
    print("1. Inicializando campana en Bonita...")
    if workflow.initialize_campaign(campana):
        
        # Registrar algunas vacunaciones
        print("\n2. Registrando vacunaciones...")
        
        registros = [
            RegistroVacunacion(
                campana_id=1,
                nombres='Juan',
                apellidos='García',
                cedula='1234567890',
                edad=72,
                sexo='M',
                lote_id=1,
                sitio_vacunacion='Centro de Salud Metropolitano',
                personal_vacunador='Enfermera Rosa',
                estado=EstadoRegistro.COMPLETO,
                observaciones='Sin reacciones adversas'
            ),
            RegistroVacunacion(
                campana_id=1,
                nombres='María',
                apellidos='Rodríguez',
                cedula='0987654321',
                edad=68,
                sexo='F',
                lote_id=1,
                sitio_vacunacion='Clínica Central',
                personal_vacunador='Dr. Luis',
                estado=EstadoRegistro.COMPLETO,
                observaciones='Reacción leve: dolor en brazo'
            )
        ]
        
        for registro in registros:
            if workflow.record_vaccination(registro):
                print(f"   ✓ {registro.nombres} {registro.apellidos} vacunado")
        
        # Obtener tareas pendientes
        print("\n3. Tareas pendientes:")
        tasks = workflow.get_pending_tasks()
        for task in tasks:
            print(f"   - {task['displayName']} (Prioridad: {task['priority']})")
        
        # Completar una tarea
        print("\n4. Completando tarea de revisión...")
        if tasks:
            approval_data = {
                'revision_aprobada': True,
                'comentarios': 'Campana aprobada para ejecución'
            }
            if workflow.complete_task(tasks[0]['id'], approval_data):
                print(f"   ✓ Tarea completada")
        
        # Obtener estado actual
        print("\n5. Estado actual de la campana:")
        status = workflow.get_campaign_status()
        for key, value in status.items():
            print(f"   - {key}: {value}")
        
        # Finalizar
        workflow.finalize()


def ejemplo_5_manejo_errores():
    """
    Ejemplo 5: Manejo de errores con mocks
    """
    print("\n" + "="*60)
    print("EJEMPLO 5: Manejo de Errores")
    print("="*60)
    
    client = BonitaMockClient()
    
    # Intento de login fallido
    print("1. Intento de login con credenciales inválidas:")
    result = client.login('wrong_user', 'wrong_password')
    print(f"   Status: {result['status_code']}")
    print(f"   Error: {result['data']['error']}")
    
    # Intento de operación sin autenticación
    print("\n2. Intento de obtener procesos sin autenticación:")
    result = client.get_processes()
    print(f"   Status: {result['status_code']}")
    print(f"   Error: {result['data']['error']}")
    
    # Login exitoso
    print("\n3. Login exitoso:")
    client.login('admin', 'admin')
    
    # Obtener proceso inexistente
    print("\n4. Intento de obtener proceso que no existe:")
    result = client.get_process_by_name('non_existent_process')
    print(f"   Status: {result['status_code']}")
    print(f"   Error: {result['data']['error']}")


def ejemplo_6_factory_singleton():
    """
    Ejemplo 6: Usar Factory para obtener instancia única
    """
    print("\n" + "="*60)
    print("EJEMPLO 6: Factory Singleton")
    print("="*60)
    
    # Obtener cliente desde factory (singleton)
    client1 = BonitaMockFactory.get_client()
    client2 = BonitaMockFactory.get_client()
    
    print(f"✓ Client 1 es el mismo que Client 2: {client1 is client2}")
    
    # Autenticar en el primer cliente
    client1.login('admin', 'admin')
    print(f"✓ Client 1 autenticado: {client1.authenticated}")
    print(f"✓ Client 2 hereda autenticación: {client2.authenticated}")
    
    # Resetear factory
    BonitaMockFactory.reset()
    client3 = BonitaMockFactory.get_client()
    print(f"✓ Client 3 después de reset es diferente: {client3 is not client1}")
    print(f"✓ Client 3 sin autenticación: {client3.authenticated}")


def run_all_examples():
    """Ejecutar todos los ejemplos"""
    print("\n" + "#"*60)
    print("# EJEMPLOS DE USO DE MOCKS DE BONITA")
    print("#"*60)
    
    ejemplo_1_cliente_basico()
    ejemplo_2_iniciar_proceso()
    ejemplo_3_servicio_integracion()
    ejemplo_4_flujo_completo()
    ejemplo_5_manejo_errores()
    ejemplo_6_factory_singleton()
    
    print("\n" + "#"*60)
    print("# FIN DE EJEMPLOS")
    print("#"*60)


if __name__ == '__main__':
    run_all_examples()
