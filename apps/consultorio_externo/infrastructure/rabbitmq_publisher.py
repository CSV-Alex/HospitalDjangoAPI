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
            f"RabbitMQ Publisher inicializado: {self.host}:{self.port} "
            f"(cola: {self.queue})"
        )
    
    def publicar_resultado(self, necesita_examen: bool) -> None:
        mensaje = "true" if necesita_examen else "false"
        
        logger.info(
            f"Publicando resultado a RabbitMQ (cola: {self.queue}): {mensaje}"
        )
        
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
            
            logger.info(f"Mensaje publicado exitosamente: {mensaje}")
            
            connection.close()
        
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(
                f"Error de conexión a RabbitMQ: {str(e)}. "
                f"Verifica que RabbitMQ esté corriendo en {self.host}:{self.port}"
            )
            raise
        
        except Exception as e:
            logger.error(f"Error al publicar resultado: {str(e)}", exc_info=True)
            raise