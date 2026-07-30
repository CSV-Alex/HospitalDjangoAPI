import json
import logging
import pika
import time
from django.conf import settings
from .services import ProcesarHospitalizacionService
from ..domain.exceptions import DomainException

logger = logging.getLogger(__name__)

RABBITMQ_CONNECTION_RETRIES = 5
RABBITMQ_RETRY_DELAY = 2
RABBITMQ_SOCKET_TIMEOUT = 5.0
RABBITMQ_RECONNECT_WAIT = 5

class RabbitMQHospitalizacionConsumer:
    """Consumer para recibir solicitudes de hospitalización desde Bonita BPM."""
    
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.vhost = settings.RABBITMQ_VHOST
        # Usar cola específica para hospitalización (o fallback)
        self.queue_entrada = getattr(settings, 'RABBITMQ_QUEUE_SOLICITUD_HOSPITALIZACION', 'solicitud_hospitalizacion')
        
        self.service = ProcesarHospitalizacionService()
        
        logger.info(
            "RabbitMQ Consumer Hospitalización inicializado: %s:%s (cola entrada: %s)",
            self.host, self.port, self.queue_entrada
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
                connection_attempts=RABBITMQ_CONNECTION_RETRIES,
                retry_delay=RABBITMQ_RETRY_DELAY,
                socket_timeout=RABBITMQ_SOCKET_TIMEOUT,
            )
            
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            
            logger.info("Conectado a RabbitMQ exitosamente")
            return connection, channel
        
        except pika.exceptions.AMQPConnectionError:
            logger.exception(
                "Error de conexión a RabbitMQ. Verifica que esté corriendo en %s:%s",
                self.host, self.port
            )
            raise
    
    def procesar_mensaje(self, ch, method, properties, body):
        try:
            mensaje_string = body.decode('utf-8')
            logger.info("Mensaje recibido en hospitalización: %s", mensaje_string)
            
            datos = json.loads(mensaje_string)
            logger.info("Datos parseados: %s", datos)
            
            self.service.procesar_solicitud(datos)
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Mensaje procesado y confirmado (ACK)")
        
        except json.JSONDecodeError:
            logger.exception("Error al parsear JSON. Contenido: %s", body)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        except DomainException:
            logger.exception("Error de validación de negocio al procesar hospitalización")
            # Se encola de nuevo en caso de error transitorio o se rechaza si es error fijo
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        except Exception:
            logger.exception("Error inesperado al procesar mensaje de hospitalización")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def escuchar(self):
        connection = None
        try:
            connection, channel = self.conectar()
            
            channel.queue_declare(queue=self.queue_entrada, durable=True)
            logger.info("Cola declarada: %s", self.queue_entrada)
            
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(
                queue=self.queue_entrada,
                on_message_callback=self.procesar_mensaje,
            )
            
            logger.info("Escuchando la cola de hospitalización: %s", self.queue_entrada)
            logger.info("Presiona Ctrl+C para detener el consumer")
            
            channel.start_consuming()
        
        except pika.exceptions.AMQPConnectionError:
            logger.exception("Conexión perdida. Reintentando en %s segundos", RABBITMQ_RECONNECT_WAIT)
            time.sleep(RABBITMQ_RECONNECT_WAIT)
            self.escuchar()
        
        except KeyboardInterrupt:
            logger.info("Consumer detenido por el usuario")
            if connection and not connection.is_closed:
                connection.close()
        
        except Exception:
            logger.exception("Error fatal en el consumer de hospitalización")
            if connection and not connection.is_closed:
                connection.close()
            raise
