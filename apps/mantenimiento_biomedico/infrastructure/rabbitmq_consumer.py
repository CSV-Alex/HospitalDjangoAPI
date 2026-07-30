import json
import logging
import pika
from django.conf import settings
from apps.mantenimiento_biomedico.application.services import ProcesarReporteService

logger = logging.getLogger(__name__)


class RabbitMQConsumer:

    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.vhost = settings.RABBITMQ_VHOST
        self.queue = settings.RABBITMQ_QUEUE_MANTENIMIENTO

        self.service = ProcesarReporteService()

        logger.info(
            f"RabbitMQ Consumer mantenimiento inicializado: {self.host}:{self.port} "
            f"(cola: {self.queue})"
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
            mensaje_string = body.decode('utf-8')

            print(f"\nMensaje recibido de Bonita ({self.queue}): {mensaje_string}")

            logger.info(f"Mensaje recibido de Bonita (cola={self.queue}): {mensaje_string}")

            datos = json.loads(mensaje_string)
            logger.info(f"Datos parseados: {datos}")

            self.service.procesar(datos)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Mensaje procesado y confirmado (ACK)")
            print("Reporte procesado correctamente\n")

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {str(e)}")
            logger.error(f"Contenido: {body}")
            print(f"Error: JSON inválido - {e}\n")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            logger.error(f"Error al procesar mensaje: {str(e)}", exc_info=True)
            print(f"Error: {e}\n")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def escuchar(self):
        connection = None
        try:
            connection, channel = self.conectar()

            channel.queue_declare(queue=self.queue, durable=True)
            logger.info(f"Cola declarada: {self.queue}")

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=self.queue,
                on_message_callback=self.procesar_mensaje,
            )

            logger.info(f"Escuchando la cola: {self.queue}")
            logger.info("Presiona Ctrl+C para detener el consumer")

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
