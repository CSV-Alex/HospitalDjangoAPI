import logging
from django.core.management.base import BaseCommand
from apps.admision_hospitalizacion.application.consumers import RabbitMQHospitalizacionConsumer

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = (
        'Inicia el Consumer de RabbitMQ para escuchar solicitudes de hospitalización de Bonita BPM. '
        'Presiona Ctrl+C para detener.'
    )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando Consumer de RabbitMQ para Hospitalización: ')
        )
        
        try:
            consumer = RabbitMQHospitalizacionConsumer()
            consumer.escuchar()
        
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('Consumer de Hospitalización detenido')
            )
        
        except Exception:
            self.stdout.write(
                self.style.ERROR('Error en el consumer de Hospitalización')
            )
            logger.exception("Error en el consumer de Hospitalización")
            raise
