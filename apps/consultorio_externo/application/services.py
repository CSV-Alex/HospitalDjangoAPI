import logging
from typing import Dict, Any

from ..domain.factories import PacienteFactory
from ..domain.exceptions import DomainException
from ..infrastructure.repositories import PacienteRepositoryDjango
from ..infrastructure.rabbitmq_publisher import RabbitMQPublisher

logger = logging.getLogger(__name__)


class RegistrarConsultaService:
    
    def __init__(
        self,
        repository: PacienteRepositoryDjango = None,
        publisher: RabbitMQPublisher = None,
    ):

        self.repository = repository or PacienteRepositoryDjango()
        self.publisher = publisher or RabbitMQPublisher()
    
    def registrar_consulta(self, datos_bonita: Dict[str, Any]) -> bool:
        try:
            logger.info(f"Iniciando registro de consulta...")
            logger.info(f"Datos recibidos: {datos_bonita}")
            
            # 1. VALIDACIÓN Y CREACIÓN DE LA ENTIDAD (usando el Factory del Dominio)
            logger.info("#### Validando y creando Entidad Paciente...")
            paciente = PacienteFactory.crear_desde_bonita(datos_bonita)
            logger.info(f"Paciente creado: {paciente}")
            
            # 2. GUARDADO EN LA BASE DE DATOS
            logger.info("#### Guardando Paciente en la base de datos...")
            self.repository.save(paciente)
            logger.info(f"Paciente guardado exitosamente")
            
            # 3. DETERMINAR SI NECESITA EXAMEN
            necesita_examen = paciente.necesita_examen.valor
            logger.info(f"#### Necesita examen: {necesita_examen}")
            
            # 4. PUBLICAR RESULTADO A RABBITMQ
            logger.info(f"#### Publicando resultado a RabbitMQ...")
            self.publisher.publicar_resultado(necesita_examen)
            logger.info(f"Resultado publicado: {necesita_examen}")
            
            logger.info("Consulta registrada de forma correcta")
            return necesita_examen
        
        except DomainException as e:
            logger.error(f"Error de negocio: {str(e)}")
            try:
                self.publisher.publicar_resultado(False)
            except Exception as pub_error:
                logger.error(f"Error al publicar fallo: {str(pub_error)}")
            raise
        
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}", exc_info=True)
            try:
                self.publisher.publicar_resultado(False)
            except Exception as pub_error:
                logger.error(f"Error al publicar fallo: {str(pub_error)}")
            raise DomainException(f"Error al registrar consulta: {str(e)}")