from abc import ABC, abstractmethod
from typing import List, Optional
from apps.mantenimiento_biomedico.domain.entities import (
    EquipoBio, Reporte, Eval,
    Solicitud, Estimacion, Presup,
    Interv,
)


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
    def delete(self, equipo_id: int) -> None:
        pass


class IReporteRepo(ABC):
    @abstractmethod
    def save(self, reporte: Reporte) -> Reporte:
        pass

    @abstractmethod
    def find_by_id(self, reporte_id: int) -> Optional[Reporte]:
        pass

    @abstractmethod
    def find_all(self) -> List[Reporte]:
        pass

    @abstractmethod
    def delete(self, reporte_id: int) -> None:
        pass


class IEvalRepo(ABC):
    @abstractmethod
    def save(self, evaluacion: Eval) -> Eval:
        pass

    @abstractmethod
    def find_by_id(self, evaluacion_id: int) -> Optional[Eval]:
        pass

    @abstractmethod
    def find_all(self) -> List[Eval]:
        pass


class ISolicitudRepo(ABC):
    @abstractmethod
    def save(self, solicitud: Solicitud) -> Solicitud:
        pass

    @abstractmethod
    def find_by_id(self, solicitud_id: int) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def find_all(self) -> List[Solicitud]:
        pass


class IEstimacionRepo(ABC):
    @abstractmethod
    def save(self, estimacion: Estimacion) -> Estimacion:
        pass

    @abstractmethod
    def find_by_id(self, estimacion_id: int) -> Optional[Estimacion]:
        pass

    @abstractmethod
    def find_all(self) -> List[Estimacion]:
        pass


class IPresupRepo(ABC):
    @abstractmethod
    def save(self, presupuesto: Presup) -> Presup:
        pass

    @abstractmethod
    def find_by_id(self, presupuesto_id: int) -> Optional[Presup]:
        pass

    @abstractmethod
    def find_all(self) -> List[Presup]:
        pass


class IIntervRepo(ABC):
    @abstractmethod
    def save(self, intervencion: Interv) -> Interv:
        pass

    @abstractmethod
    def find_by_id(self, intervencion_id: int) -> Optional[Interv]:
        pass

    @abstractmethod
    def find_by_equipo_id(self, equipo_id: int) -> List[Interv]:
        pass

    @abstractmethod
    def find_all(self) -> List[Interv]:
        pass
