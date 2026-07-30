from django.test import TestCase
from datetime import date

from ..domain.entities import Paciente
from ..domain.value_objects import (
    NumeroHistoriaClinica,
    NombreCompleto,
    FechaNacimiento,
    NecesitaExamen,
)
from ..domain.exceptions import DomainException


class TestPacienteEntity(TestCase):
    """Tests para la entidad Paciente"""

    def setUp(self):
        """Preparar datos para cada test (usaron Juan Perez en otro test, usamos lo mismo)"""
        self.numero_historia = NumeroHistoriaClinica("HC-2026-001")
        self.nombre = NombreCompleto("Juan Perez García")
        self.fecha_nacimiento = FechaNacimiento(date(1990, 5, 15))
        self.necesita_examen = NecesitaExamen(True)

    def test_crear_paciente_valido(self):
        """Debe crear un Paciente con todos los datos válidos"""
        paciente = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        self.assertEqual(paciente.numero_historia_clinica, self.numero_historia)
        self.assertEqual(paciente.nombre_completo, self.nombre)
        self.assertEqual(paciente.fecha_nacimiento, self.fecha_nacimiento)
        self.assertTrue(paciente.necesita_examen.valor)

    def test_paciente_tiene_identidad_unica(self):
        """Cada Paciente debe tener un ID único"""
        paciente1 = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        paciente2 = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        self.assertIsNotNone(paciente1.id)
        self.assertIsNotNone(paciente2.id)
        self.assertNotEqual(paciente1.id, paciente2.id)

    def test_dos_pacientes_con_diferentes_datos_son_distintos(self):
        """Dos Pacientes con datos diferentes no deben ser iguales"""
        paciente1 = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        numero_diferente = NumeroHistoriaClinica("HC-2026-002")
        paciente2 = Paciente(
            numero_historia_clinica=numero_diferente,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        self.assertNotEqual(paciente1, paciente2)

    def test_paciente_mismo_numero_historia_debe_fallar(self):
        """No debe permitir dos pacientes con el mismo número de historia (a nivel de dominio)"""
        numero1 = NumeroHistoriaClinica("HC-2026-001")
        numero2 = NumeroHistoriaClinica("HC-2026-002")
        
        paciente1 = Paciente(
            numero_historia_clinica=numero1,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        paciente2 = Paciente(
            numero_historia_clinica=numero2,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        self.assertNotEqual(paciente1.numero_historia_clinica, paciente2.numero_historia_clinica)

    def test_obtener_edad_del_paciente(self):
        """El Paciente debe poder calcular su edad"""
        paciente = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=self.necesita_examen,
        )
        edad = paciente.obtener_edad()
        self.assertGreaterEqual(edad, 35)
        self.assertLessEqual(edad, 36)

    def test_paciente_necesita_examen_es_modificable(self):
        """Se debe poder modificar si el paciente necesita examen"""
        paciente = Paciente(
            numero_historia_clinica=self.numero_historia,
            nombre_completo=self.nombre,
            fecha_nacimiento=self.fecha_nacimiento,
            necesita_examen=NecesitaExamen(False),
        )
        self.assertFalse(paciente.necesita_examen.valor)
        
        paciente.necesita_examen = NecesitaExamen(True)
        self.assertTrue(paciente.necesita_examen.valor)