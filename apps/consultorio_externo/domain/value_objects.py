from datetime import date, datetime
from typing import Union

from .exceptions import (
    DomainException,
    NumeroHistoriaClinicaInvalidoException,
    NombreCompletoInvalidoException,
    FechaNacimientoInvalidaException,
)

class ValueObject:
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class NumeroHistoriaClinica(ValueObject):

    def __init__(self, valor: str):

        if not valor or (isinstance(valor, str) and valor.strip() == ""):
            raise NumeroHistoriaClinicaInvalidoException(
                "El número de historia clínica no puede estar vacío"
            )
        
        if not isinstance(valor, str):
            raise NumeroHistoriaClinicaInvalidoException(
                f"El número de historia clínica debe ser un string, recibido: {type(valor)}"
            )
        
        self.valor = valor.strip()


class NombreCompleto(ValueObject):
    
    MIN_LENGTH = 3
    MAX_LENGTH = 255
    
    def __init__(self, valor: str):

        if not valor or (isinstance(valor, str) and valor.strip() == ""):
            raise NombreCompletoInvalidoException(
                "El nombre completo no puede estar vacío"
            )
        
        if not isinstance(valor, str):
            raise NombreCompletoInvalidoException(
                f"El nombre debe ser un string, recibido: {type(valor)}"
            )
        
        # Normalizar: eliminar espacios extras
        nombre_normalizado = " ".join(valor.split())
        
        if len(nombre_normalizado) < self.MIN_LENGTH:
            raise NombreCompletoInvalidoException(
                f"El nombre debe tener al menos {self.MIN_LENGTH} caracteres. "
                f"Recibido: {len(nombre_normalizado)} caracteres"
            )
        
        if len(nombre_normalizado) > self.MAX_LENGTH:
            raise NombreCompletoInvalidoException(
                f"El nombre no puede exceder {self.MAX_LENGTH} caracteres. "
                f"Recibido: {len(nombre_normalizado)} caracteres"
            )
        
        self.valor = nombre_normalizado


class FechaNacimiento(ValueObject):
    MAX_AGE_YEARS = 150
    
    def __init__(self, valor: Union[date, datetime]):

        if isinstance(valor, datetime):
            valor = valor.date()
        
        if not isinstance(valor, date):
            raise FechaNacimientoInvalidaException(
                f"La fecha debe ser un objeto date o datetime, recibido: {type(valor)}"
            )
        
        # No puede ser en el futuro
        if valor > date.today():
            raise FechaNacimientoInvalidaException(
                f"La fecha de nacimiento no puede ser en el futuro. Recibido: {valor}"
            )
        
        # No puede ser demasiado antigua
        edad = self._calcular_edad(valor)
        if edad > self.MAX_AGE_YEARS:
            raise FechaNacimientoInvalidaException(
                f"La edad no puede ser mayor a {self.MAX_AGE_YEARS} años. "
                f"Edad calculada: {edad} años"
            )
        
        self.valor = valor
    
    @staticmethod
    def _calcular_edad(fecha_nacimiento: date) -> int:
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year
        
        # Restar 1 si aún no ha pasado el cumpleaños este anio
        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1
        
        return edad
    
    def calcular_edad(self) -> int:
        return self._calcular_edad(self.valor)


class NecesitaExamen(ValueObject):
    
    def __init__(self, valor: bool):
        if not isinstance(valor, bool):
            raise DomainException(
                f"NecesitaExamen debe ser un booleano, recibido: {type(valor)}"
            )
        
        self.valor = valor