from abc import ABC, abstractmethod
from typing import List, Optional
from apps.campana_vacunacion.domain.entities import (
    Vacuna, Lote, Campana, RegistroVacunacion,Poblacion,
)


class IVacunaRepo(ABC):
    @abstractmethod
    def save(self, vacuna: Vacuna) -> Vacuna:
        pass

    @abstractmethod
    def find_by_id(self, vacuna_id: int) -> Optional[Vacuna]:
        pass

    @abstractmethod
    def find_all(self) -> List[Vacuna]:
        pass

    @abstractmethod
    def delete(self, vacuna_id: int) -> None:
        pass


class ILoteRepo(ABC):
    @abstractmethod
    def save(self, lote: Lote) -> Lote:
        pass

    @abstractmethod
    def find_by_id(self, lote_id: int) -> Optional[Lote]:
        pass

    @abstractmethod
    def find_all(self) -> List[Lote]:
        pass

    @abstractmethod
    def find_by_vacuna(self, vacuna_id: int) -> List[Lote]:
        pass

    @abstractmethod
    def delete(self, lote_id: int) -> None:
        pass


class ICampanaRepo(ABC):
    @abstractmethod
    def save(self, campana: Campana) -> Campana:
        pass

    @abstractmethod
    def find_by_id(self, campana_id: int) -> Optional[Campana]:
        pass

    @abstractmethod
    def find_all(self) -> List[Campana]:
        pass

    @abstractmethod
    def delete(self, campana_id: int) -> None:
        pass


class IRegistroVacunacionRepo(ABC):
    @abstractmethod
    def save(self, registro: RegistroVacunacion) -> RegistroVacunacion:
        pass

    @abstractmethod
    def find_by_id(self, registro_id: int) -> Optional[RegistroVacunacion]:
        pass

    @abstractmethod
    def find_all(self) -> List[RegistroVacunacion]:
        pass

    @abstractmethod
    def find_by_campana(self, campana_id: int) -> List[RegistroVacunacion]:
        pass

    @abstractmethod
    def delete(self, registro_id: int) -> None:
        pass


class IPoblacionRepo(ABC):
    @abstractmethod
    def save(self, poblacion: Poblacion) -> Poblacion:
        pass

    @abstractmethod
    def find_by_id(self, poblacion_id: int) -> Optional[Poblacion]:
        pass

    @abstractmethod
    def find_all(self) -> List[Poblacion]:
        pass

    @abstractmethod
    def find_by_campana(self, campana_id: int) -> List[Poblacion]:
        pass

    @abstractmethod
    def delete(self, poblacion_id: int) -> None:
        pass
