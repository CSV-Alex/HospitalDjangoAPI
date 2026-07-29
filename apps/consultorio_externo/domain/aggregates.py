from typing import List, Optional
from datetime import date

from .entities import Paciente
from .value_objects import (
    NumeroHistoriaClinica,
    NombreCompleto,
    FechaNacimiento,
    NecesitaExamen,
)
from .exceptions import PacienteInvalidoException


class PacienteAggregate:
    def __init__(self, paciente: Paciente):
        if not isinstance(paciente, Paciente):
            raise PacienteInvalidoException(
                f"paciente debe ser una instancia de Paciente, "
                f"recibido: {type(paciente)}"
            )
        
        self.paciente = paciente
    
    def obtener_paciente(self) -> Paciente:
        return self.paciente
    
    def necesita_laboratorio(self) -> bool:
        return self.paciente.necesita_examen.valor