import logging
from django.core.management.base import BaseCommand
from apps.mantenimiento_biomedico.infrastructure.rabbitmq_consumer import RabbitMQConsumer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        'Inicia el Consumer de RabbitMQ para reportes de mantenimiento. '
        'Presiona Ctrl+C para detener.'
    )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando Consumer de RabbitMQ para mantenimiento')
        )
        self.stdout.write('  Escuchando mensajes de Bonita en cola: mantenimiento_reporte')
        self.stdout.write('  Presiona Ctrl+C para detener\n')

        try:
            consumer = RabbitMQConsumer()
            consumer.escuchar()

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('Consumer detenido')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            logger.error(f"Error en el consumer: {str(e)}", exc_info=True)
            raise
