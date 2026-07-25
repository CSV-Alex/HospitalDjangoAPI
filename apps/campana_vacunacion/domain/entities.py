from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from apps.campana_vacunacion.domain.enums import (
    EstadoCampana, TipoVacuna, EstadoLote,
    EstadoRegistro,
)


@dataclass
class Vacuna:
    id: Optional[int] = None
    nombre: str = ""
    tipo: TipoVacuna = TipoVacuna.OTROS
    fabricante: str = ""
    descripcion: str = ""
    tempconserv_min: float = 0.0
    tempconserv_max: float = 0.0


@dataclass
class Lote:
    id: Optional[int] = None
    vacuna: Optional[Vacuna] = None
    vacuna_id: Optional[int] = None
    num_lote: str = ""
    fecha_fab: Optional[date] = None
    fecha_venc: Optional[date] = None
    cantidad: int = 0
    cantidad_usada: int = 0
    estado: EstadoLote = EstadoLote.DISP


@dataclass
class Campana:
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    objetivo: str = ""
    poblacion_objetivo: str = ""
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    vacuna: Optional[Vacuna] = None
    vacuna_id: Optional[int] = None
    responsable: str = ""
    estado: EstadoCampana = EstadoCampana.PLANIF
    fecha_creacion: datetime = field(default_factory=datetime.now)


@dataclass
class RegistroVacunacion:
    id: Optional[int] = None
    campana: Optional[Campana] = None
    campana_id: Optional[int] = None
    nombres: str = ""
    apellidos: str = ""
    cedula: str = ""
    edad: int = 0
    sexo: str = ""
    lote: Optional[Lote] = None
    lote_id: Optional[int] = None
    fecha_vacunacion: datetime = field(default_factory=datetime.now)
    sitio_vacunacion: str = ""
    personal_vacunador: str = ""
    estado: EstadoRegistro = EstadoRegistro.PEND
    observaciones: Optional[str] = None


@dataclass
class Poblacion:
    id: Optional[int] = None
    campana: Optional[Campana] = None
    campana_id: Optional[int] = None
    grupo_edad_min: int = 0
    grupo_edad_max: int = 150
    descripcion: str = ""
    cantidad_estimada: int = 0
    cantidad_vacunada: int = 0
