from dataclasses import dataclass
from .exceptions import ValidacionException

@dataclass(frozen=True)
class NumeroOrden:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValidacionException("El número de orden no puede estar vacío")

@dataclass(frozen=True)
class DniPaciente:
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor) != 8 or not self.valor.isdigit():
            raise ValidacionException("El DNI debe tener 8 dígitos numéricos")

@dataclass(frozen=True)
class Especialidad:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValidacionException("La especialidad no puede estar vacía")

@dataclass(frozen=True)
class CodigoCama:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValidacionException("El código de cama no puede estar vacío")
