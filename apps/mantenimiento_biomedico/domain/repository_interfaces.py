from abc import ABC, abstractmethod
from typing import List, Optional
from apps.mantenimiento_biomedico.domain.entities import EquipoBio, Reporte


class IEquipoRepo(ABC):
    @abstractmethod
    def save(self, equipo: EquipoBio) -> EquipoBio:
        pass

    @abstractmethod
    def find_by_id(self, equipo_id: int) -> Optional[EquipoBio]:
        pass

    @abstractmethod
    def find_all(self) -> List[EquipoBio]:
        pass

    @abstractmethod
    def find_by_codigo(self, codigo: str) -> Optional[EquipoBio]:
        pass


class IReporteRepo(ABC):
    @abstractmethod
    def find_by_id(self, reporte_id: int) -> Optional[Reporte]:
        pass

    @abstractmethod
    def find_all(self) -> List[Reporte]:
        pass

    @abstractmethod
    def delete(self, reporte_id: int) -> None:
        pass
