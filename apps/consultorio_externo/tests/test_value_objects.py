from django.test import TestCase
from datetime import date

from ..domain.value_objects import (
    NumeroHistoriaClinica,
    NombreCompleto,
    FechaNacimiento,
    NecesitaExamen,
)
from ..domain.exceptions import DomainException


class TestNumeroHistoriaClinica(TestCase):
    """Tests para el Value Object NumeroHistoriaClinica"""

    def test_crear_numero_historia_clinica_valido(self):
        """Debe crear un NumeroHistoriaClinica con un valor válido"""
        numero = NumeroHistoriaClinica("HC-2026-001")
        self.assertEqual(numero.valor, "HC-2026-001")

    def test_numero_historia_clinica_no_puede_estar_vacio(self):
        """Debe lanzar excepción si el número está vacío"""
        with self.assertRaises(DomainException):
            NumeroHistoriaClinica("")

    def test_numero_historia_clinica_no_puede_ser_none(self):
        """Debe lanzar excepción si el número es None"""
        with self.assertRaises(DomainException):
            NumeroHistoriaClinica(None)

    def test_numero_historia_clinica_igualdad(self):
        """Dos Value Objects con el mismo valor deben ser iguales"""
        numero1 = NumeroHistoriaClinica("HC-2026-001")
        numero2 = NumeroHistoriaClinica("HC-2026-001")
        self.assertEqual(numero1, numero2)

    def test_numero_historia_clinica_desigualdad(self):
        """Dos Value Objects con diferente valor deben ser distintos"""
        numero1 = NumeroHistoriaClinica("HC-2026-001")
        numero2 = NumeroHistoriaClinica("HC-2026-002")
        self.assertNotEqual(numero1, numero2)


class TestNombreCompleto(TestCase):
    """Tests para el Value Object NombreCompleto"""

    def test_crear_nombre_completo_valido(self):
        """Debe crear un NombreCompleto con un valor válido"""
        nombre = NombreCompleto("Juan Perez García")
        self.assertEqual(nombre.valor, "Juan Perez García")

    def test_nombre_completo_no_puede_estar_vacio(self):
        """Debe lanzar excepción si el nombre está vacío"""
        with self.assertRaises(DomainException):
            NombreCompleto("")

    def test_nombre_completo_minimo_caracteres(self):
        """Debe lanzar excepción si el nombre tiene menos de 3 caracteres"""
        with self.assertRaises(DomainException):
            NombreCompleto("AB")

    def test_nombre_completo_maximo_caracteres(self):
        """Debe lanzar excepción si el nombre tiene más de 255 caracteres"""
        nombre_largo = "A" * 256
        with self.assertRaises(DomainException):
            NombreCompleto(nombre_largo)

    def test_nombre_completo_normalizado(self):
        """El nombre debe ser normalizado (sin espacios extra)"""
        nombre = NombreCompleto("  Juan   Perez  ")
        self.assertEqual(nombre.valor, "Juan Perez")


class TestFechaNacimiento(TestCase):
    """Tests para el Value Object FechaNacimiento"""

    def test_crear_fecha_nacimiento_valida(self):
        """Debe crear una FechaNacimiento con una fecha válida"""
        fecha = FechaNacimiento(date(1990, 5, 15))
        self.assertEqual(fecha.valor, date(1990, 5, 15))

    def test_fecha_nacimiento_no_puede_ser_futura(self):
        """Debe lanzar excepción si la fecha es en el futuro"""
        fecha_futura = date(2030, 1, 1)
        with self.assertRaises(DomainException):
            FechaNacimiento(fecha_futura)

    def test_fecha_nacimiento_no_puede_ser_muy_antigua(self):
        """Debe lanzar excepción si la fecha es más de 150 años atrás"""
        fecha_muy_antigua = date(1800, 1, 1)
        with self.assertRaises(DomainException):
            FechaNacimiento(fecha_muy_antigua)

    def test_calcular_edad(self):
        """Debe calcular correctamente la edad"""
        fecha = FechaNacimiento(date(1990, 5, 15))
        edad = fecha.calcular_edad()
        self.assertGreaterEqual(edad, 35)
        self.assertLessEqual(edad, 36)


class TestNecesitaExamen(TestCase):
    """Tests para el Value Object NecesitaExamen"""

    def test_crear_necesita_examen_verdadero(self):
        """Debe crear un NecesitaExamen con valor True"""
        necesita = NecesitaExamen(True)
        self.assertTrue(necesita.valor)

    def test_crear_necesita_examen_falso(self):
        """Debe crear un NecesitaExamen con valor False"""
        necesita = NecesitaExamen(False)
        self.assertFalse(necesita.valor)

    def test_necesita_examen_igualdad(self):
        """Dos Value Objects con el mismo valor deben ser iguales"""
        necesita1 = NecesitaExamen(True)
        necesita2 = NecesitaExamen(True)
        self.assertEqual(necesita1, necesita2)