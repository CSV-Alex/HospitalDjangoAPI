from abc import ABC, abstractmethod
from typing import List, Optional
from apps.pruebas_laboratorio.domain.entities import (
    Paciente, SolicitudPrueba, ResultadoPrueba
)


class IPacienteRepo(ABC):
    @abstractmethod
    def save(self, equipo: Paciente) -> Paciente:
        pass

    @abstractmethod
    def find_by_id(self, equipo_id: int) -> Optional[Paciente]:
        pass

    @abstractmethod
    def find_all(self) -> List[Paciente]:
        pass

    @abstractmethod
    def delete(self, equipo_id: int) -> None:
        pass

class ISolicitudPruebaRepo(ABC):
    @abstractmethod
    def save(self, solicitud: SolicitudPrueba) -> SolicitudPrueba:
        pass

    @abstractmethod
    def find_by_id(self, solicitud_id: int) -> Optional[SolicitudPrueba]:
        pass

    @abstractmethod
    def find_all(self) -> List[SolicitudPrueba]:
        pass

    @abstractmethod
    def delete(self, solicitud_id: int) -> None:
        pass

class IResultadoPruebaRepo(ABC):
    @abstractmethod
    def save(self, resultado: ResultadoPrueba) -> ResultadoPrueba:
        pass

    @abstractmethod
    def find_by_id(self, resultado_id: int) -> Optional[ResultadoPrueba]:
        pass

    @abstractmethod
    def find_all(self) -> List[ResultadoPrueba]:
        pass

    @abstractmethod
    def delete(self, resultado_id: int) -> None:
        pass