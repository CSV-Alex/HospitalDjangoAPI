import logging
from typing import Dict, Any

from ..domain.factories import HospitalizacionFactory
from ..domain.exceptions import DomainException
from ..infrastructure.repositories import HospitalizacionRepositoryDjango
from ..infrastructure.rabbitmq_publisher import RabbitMQHospitalizacionPublisher

logger = logging.getLogger(__name__)

class ProcesarHospitalizacionService:
    """Servicio de aplicación para coordinar el proceso de admisión y hospitalización."""
    
    def __init__(
        self,
        repository: HospitalizacionRepositoryDjango = None,
        publisher: RabbitMQHospitalizacionPublisher = None,
    ):
        self.repository = repository or HospitalizacionRepositoryDjango()
        self.publisher = publisher or RabbitMQHospitalizacionPublisher()
    
    def procesar_solicitud(self, datos_bonita: Dict[str, Any]) -> bool:
        try:
            logger.info("Iniciando procesamiento de solicitud de hospitalización...")
            logger.info("Datos recibidos: %s", datos_bonita)
            
            # 1. VALIDACIÓN Y CREACIÓN DE LA ENTIDAD
            logger.info("#### Construyendo Entidad de Dominio (HospitalizacionRequest)...")
            solicitud = HospitalizacionFactory.crear_desde_bonita(datos_bonita)
            logger.info("Solicitud creada: %s", solicitud)
            
            # 2. PROCESAMIENTO Y GUARDADO EN LA BASE DE DATOS
            logger.info("#### Registrando hospitalización en la base de datos...")
            self.repository.save(solicitud)
            logger.info("Hospitalización registrada exitosamente")
            
            # 3. PUBLICAR RESULTADO A RABBITMQ (Éxito)
            logger.info("#### Publicando resultado (Éxito) a RabbitMQ...")
            self.publisher.publicar_resultado(exito=True)
            
            return True
        
        except DomainException as e:
            logger.warning("Error de negocio al procesar solicitud: %s", str(e))
            self._publicar_fallo()
            raise
        
        except Exception as e:
            logger.exception("Error inesperado al procesar solicitud de hospitalización")
            self._publicar_fallo()
            raise DomainException("Error interno al procesar hospitalización")
            
    def _publicar_fallo(self):
        try:
            logger.info("Publicando resultado (Fallo) a RabbitMQ...")
            self.publisher.publicar_resultado(exito=False)
        except Exception:
            logger.exception("Error al intentar publicar mensaje de fallo en RabbitMQ")
