from django.test import TestCase
from datetime import date

from ..domain.factories import PacienteFactory
from ..domain.exceptions import DomainException


class TestPacienteFactory(TestCase):
    """Tests para el Factory de Paciente"""

    def test_crear_paciente_desde_dict_valido(self):
        """Debe crear un Paciente válido desde un diccionario"""
        datos = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": date(1990, 5, 15),
            "necesitaExamen": True,
        }
        paciente = PacienteFactory.crear_desde_bonita(datos)
        
        self.assertEqual(paciente.numero_historia_clinica.valor, "HC-2026-001")
        self.assertEqual(paciente.nombre_completo.valor, "Juan Perez García")
        self.assertEqual(paciente.fecha_nacimiento.valor, date(1990, 5, 15))
        self.assertTrue(paciente.necesita_examen.valor)

    def test_factory_lanza_excepcion_si_falta_numero_historia(self):
        """Debe lanzar excepción si falta numeroHistoriaClinica"""
        datos = {
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": date(1990, 5, 15),
            "necesitaExamen": True,
        }
        with self.assertRaises((DomainException, KeyError)):
            PacienteFactory.crear_desde_bonita(datos)

    def test_factory_lanza_excepcion_si_falta_nombre(self):
        """Debe lanzar excepción si falta nombreCompleto"""
        datos = {
            "numeroHistoriaClinica": "HC-2026-001",
            "fechaNacimiento": date(1990, 5, 15),
            "necesitaExamen": True,
        }
        with self.assertRaises((DomainException, KeyError)):
            PacienteFactory.crear_desde_bonita(datos)

    def test_factory_lanza_excepcion_si_falta_fecha_nacimiento(self):
        """Debe lanzar excepción si falta fechaNacimiento"""
        datos = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "necesitaExamen": True,
        }
        with self.assertRaises((DomainException, KeyError)):
            PacienteFactory.crear_desde_bonita(datos)

    def test_factory_lanza_excepcion_si_falta_necesita_examen(self):
        """Debe lanzar excepción si falta necesitaExamen"""
        datos = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": date(1990, 5, 15),
        }
        with self.assertRaises((DomainException, KeyError)):
            PacienteFactory.crear_desde_bonita(datos)

    def test_factory_convierte_fecha_string_a_date(self):
        """Debe convertir fecha en string a objeto date"""
        datos = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": "1990-05-15",  # String
            "necesitaExamen": True,
        }
        paciente = PacienteFactory.crear_desde_bonita(datos)
        self.assertEqual(paciente.fecha_nacimiento.valor, date(1990, 5, 15))

    def test_factory_maneja_necesita_examen_como_string(self):
        """Debe convertir 'true'/'false' en string a booleano"""
        datos_true = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": date(1990, 5, 15),
            "necesitaExamen": "true",  # String
        }
        paciente = PacienteFactory.crear_desde_bonita(datos_true)
        self.assertTrue(paciente.necesita_examen.valor)

        datos_false = {
            "numeroHistoriaClinica": "HC-2026-001",
            "nombreCompleto": "Juan Perez García",
            "fechaNacimiento": date(1990, 5, 15),
            "necesitaExamen": "false",  # String
        }
        paciente = PacienteFactory.crear_desde_bonita(datos_false)
        self.assertFalse(paciente.necesita_examen.valor)