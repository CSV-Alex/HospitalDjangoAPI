import json
import pika
from django.core.management.base import BaseCommand
from farmacia.models import Medicamento # Asegúrate de importar tu modelo

class Command(BaseCommand):
    help = 'Inicia el consumidor de RabbitMQ para Farmacia'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='bpm_to_django_farmacia')
        channel.queue_declare(queue='django_to_bpm_farmacia')

        def callback(ch, method, properties, body):
            print(" [x] Mensaje recibido de Bonita")
            datos_receta = json.loads(body)
            medicamentos_solicitados = datos_receta.get('medicamentos', [])
            
            exito = True
            
            for item in medicamentos_solicitados:
                try:
                    med = Medicamento.objects.get(id=item['id'])
                    if med.stock >= item['cantidad']:
                        med.stock -= item['cantidad']
                        med.save()
                    else:
                        exito = False
                        break
                except Medicamento.DoesNotExist:
                    exito = False
                    break

            respuesta = {
                'id_instancia_bpm': datos_receta.get('id_instancia_bpm'),
                'estado': 'PROCESADO' if exito else 'SIN_STOCK'
            }
            
            channel.basic_publish(
                exchange='',
                routing_key='django_to_bpm_farmacia',
                body=json.dumps(respuesta)
            )
            print(f" [x] Respuesta enviada: {respuesta['estado']}")

        channel.basic_consume(queue='bpm_to_django_farmacia', on_message_callback=callback, auto_ack=True)
        print(' [*] Esperando mensajes de Bonita. Para salir presiona CTRL+C')
        channel.start_consuming()