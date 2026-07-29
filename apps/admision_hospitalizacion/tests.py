from django.test import TestCase
from .models import Paciente, Cama, OrdenInternamiento

class ModelTests(TestCase):
    def test_paciente_creation(self):
        paciente = Paciente.objects.create(
            dni='12345678',
            nombres='Juan',
            apellidos='Perez',
            fecha_nacimiento='1980-01-01'
        )
        self.assertEqual(paciente.nombres, 'Juan')
        self.assertEqual(str(paciente), 'Juan Perez')

    def test_cama_disponible(self):
        cama = Cama.objects.create(numero='101', especialidad='Medicina Interna')
        self.assertTrue(cama.disponible)
        self.assertEqual(str(cama), 'Cama 101 - Medicina Interna')
