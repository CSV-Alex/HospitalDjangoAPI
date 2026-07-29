import json
import logging
import pika
from django.conf import settings
from .services import RegistrarConsultaService
from ..domain.exceptions import DomainException

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.vhost = settings.RABBITMQ_VHOST
        self.queue_entrada = settings.RABBITMQ_QUEUE_SOLICITUD_CONSULTORIO
        
        self.service = RegistrarConsultaService()
        
        logger.info(
            f"RabbitMQ Consumer inicializado: {self.host}:{self.port} "
            f"(cola entrada: {self.queue_entrada})"
        )
    
    def conectar(self):
        try:
            logger.info(f"Conectando a RabbitMQ: {self.host}:{self.port}...")
            
            credentials = pika.PlainCredentials(self.username, self.password)
            connection_params = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=credentials,
                connection_attempts=5,
                retry_delay=2,
                socket_timeout=5.0,
            )
            
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            
            logger.info("Conectado a RabbitMQ exitosamente")
            return connection, channel
        
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(
                f"Error de conexión a RabbitMQ: {str(e)}. "
                f"Verifica que RabbitMQ esté corriendo en {self.host}:{self.port}"
            )
            raise
    
    def procesar_mensaje(self, ch, method, properties, body):
        try:
            # Decodificar el mensaje
            mensaje_string = body.decode('utf-8')
            logger.info(f"Mensaje recibido: {mensaje_string}")
            
            # Parsear JSON
            datos = json.loads(mensaje_string)
            logger.info(f"Datos parseados: {datos}")
            
            # Procesar con el Servicio de Aplicación
            self.service.registrar_consulta(datos)
            
            # Confirmar el mensaje
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Mensaje procesado y confirmado (ACK)")
        
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {str(e)}")
            logger.error(f"Contenido: {body}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        except DomainException as e:
            logger.error(f"Error de validación de negocio: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        except Exception as e:
            logger.error(f"Error inesperado al procesar mensaje: {str(e)}", exc_info=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def escuchar(self):
        connection = None
        try:
            connection, channel = self.conectar()
            
            channel.queue_declare(queue=self.queue_entrada, durable=True)
            logger.info(f"Cola declarada: {self.queue_entrada}")
            
            channel.basic_qos(prefetch_count=1)
            
            # Registrar el callback
            channel.basic_consume(
                queue=self.queue_entrada,
                on_message_callback=self.procesar_mensaje,
            )
            
            logger.info(f"Escuchando la cola: {self.queue_entrada}")
            logger.info("Presiona Ctrl+C para detener el consumer")
            
            # Iniciar a escuchar
            channel.start_consuming()
        
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Conexión perdida: {str(e)}")
            logger.info("Reintentando en 5 segundos...")
            import time
            time.sleep(5)
            self.escuchar()
        
        except KeyboardInterrupt:
            logger.info("Consumer detenido por el usuario")
            if connection and not connection.is_closed:
                connection.close()
        
        except Exception as e:
            logger.error(f"Error fatal: {str(e)}", exc_info=True)
            if connection and not connection.is_closed:
                connection.close()
            raise