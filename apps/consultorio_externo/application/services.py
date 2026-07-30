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
            logger.info("Iniciando registro de consulta...")
            logger.info("Datos recibidos: %s", datos_bonita)
            
            # 1. VALIDACIÓN Y CREACIÓN DE LA ENTIDAD (usando el Factory del Dominio)
            logger.info("#### Validando y creando Entidad Paciente...")
            paciente = PacienteFactory.crear_desde_bonita(datos_bonita)
            logger.info("Paciente creado: %s", paciente)
            
            # 2. GUARDADO EN LA BASE DE DATOS
            logger.info("#### Guardando Paciente en la base de datos...")
            self.repository.save(paciente)
            logger.info("Paciente guardado exitosamente")
            
            # 3. DETERMINAR SI NECESITA EXAMEN
            necesita_examen = paciente.necesita_examen.valor
            logger.info("Necesita examen: %s", necesita_examen)
            
            # 4. PUBLICAR RESULTADO A RABBITMQ
            logger.info("#### Publicando resultado a RabbitMQ...")
            self.publisher.publicar_resultado(necesita_examen)
            logger.info("Resultado publicado: %s", necesita_examen)
            
            logger.info("Consulta registrada de forma correcta")
            return necesita_examen
        
        except DomainException:
            logger.exception("Error de negocio al registrar consulta")
            try:
                self.publisher.publicar_resultado(False)
            except Exception:
                logger.exception("Error al publicar fallo")
            raise
        
        except Exception:
            logger.exception("Error inesperado al registrar consulta")
            try:
                self.publisher.publicar_resultado(False)
            except Exception:
                logger.exception("Error al publicar fallo")
            raise DomainException("Error al registrar consulta")