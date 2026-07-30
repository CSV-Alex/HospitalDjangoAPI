from abc import ABC, abstractmethod
from typing import Optional, List

from .entities import Paciente
from .value_objects import NumeroHistoriaClinica


class PacienteRepository(ABC):
    
    @abstractmethod
    def save(self, paciente: Paciente) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, paciente_id: str) -> Optional[Paciente]:
        pass
    
    @abstractmethod
    def find_by_numero_historia_clinica(
        self, numero_historia: NumeroHistoriaClinica
    ) -> Optional[Paciente]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Paciente]:
        pass
    
    @abstractmethod
    def update(self, paciente: Paciente) -> None:
        pass
    
    @abstractmethod
    def delete(self, paciente_id: str) -> None:
        pass