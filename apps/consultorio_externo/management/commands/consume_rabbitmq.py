import logging
from django.core.management.base import BaseCommand
from apps.consultorio_externo.application.consumers import RabbitMQConsumer

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = (
        'Inicia el Consumer de RabbitMQ para escuchar solicitudes de Bonita. '
        'Presiona Ctrl+C para detener.'
    )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando Consumer de RabbitMQ: ')
        )
        
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