import logging
import pika
from django.conf import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.vhost = settings.RABBITMQ_VHOST
        self.queue = settings.RABBITMQ_QUEUE_EVENTO_CONSULTORIO
        
        logger.info(
            "RabbitMQ Publisher inicializado: %s:%s (cola: %s)",
            self.host, self.port, self.queue
        )
    
    def publicar_resultado(self, necesita_examen: bool) -> None:
        mensaje = "true" if necesita_examen else "false"
        
        logger.info("Publicando resultado a RabbitMQ (cola: %s): %s", self.queue, mensaje)
        
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            connection_params = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=2,
                socket_timeout=5.0,
            )
            
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            channel.queue_declare(queue=self.queue, durable=True)
            
            # Publicar el mensaje
            channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=mensaje.encode('utf-8'),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    content_type='text/plain',
                ),
            )
            
            logger.info("Mensaje publicado exitosamente: %s", mensaje)
            
            connection.close()
        
        except pika.exceptions.AMQPConnectionError:
            logger.exception(
                "Error de conexión a RabbitMQ. "
                "Verifica que esté corriendo en %s:%s",
                self.host, self.port
            )
            raise
        
        except Exception:
            logger.exception("Error al publicar resultado")
            raise