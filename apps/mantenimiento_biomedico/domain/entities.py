from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from apps.mantenimiento_biomedico.domain.enums import (
    TipoEquipo, EstadoEq, EstadoRep,
    EstadoSol, EstadoPresup, TipoInterv,
)


@dataclass
class EquipoBio:
    id: Optional[int] = None
    codigo: str = ""
    nombre: str = ""
    tipo: TipoEquipo = TipoEquipo.OTROS
    fabricante: str = ""
    modelo: str = ""
    num_serie: str = ""
    ubicacion: str = ""
    fecha_adq: Optional[date] = None
    fecha_ult_calib: Optional[date] = None
    estado: EstadoEq = EstadoEq.OPER


@dataclass
class Reporte:
    id: Optional[int] = None
    equipo: Optional[EquipoBio] = None
    equipo_id: Optional[int] = None
    descripcion: str = ""
    reportado_por: str = ""
    fecha: datetime = field(default_factory=datetime.now)
    estado: EstadoRep = EstadoRep.PEND


@dataclass
class Eval:
    id: Optional[int] = None
    reporte: Optional[Reporte] = None
    reporte_id: Optional[int] = None
    tecnico: str = ""
    diagnostico: str = ""
    reemplazo: bool = False
    fecha: datetime = field(default_factory=datetime.now)


@dataclass
class Solicitud:
    id: Optional[int] = None
    eval: Optional[Eval] = None
    eval_id: Optional[int] = None
    equipo: Optional[EquipoBio] = None
    equipo_id: Optional[int] = None
    motivo: str = ""
    fecha: datetime = field(default_factory=datetime.now)
    estado: EstadoSol = EstadoSol.PEND


@dataclass
class Estimacion:
    id: Optional[int] = None
    solicitud: Optional[Solicitud] = None
    solicitud_id: Optional[int] = None
    precio: Decimal = Decimal("0.00")
    proveedor: str = ""
    detalle: str = ""
    fecha: datetime = field(default_factory=datetime.now)


@dataclass
class Presup:
    id: Optional[int] = None
    estimacion: Optional[Estimacion] = None
    estimacion_id: Optional[int] = None
    num_doc: str = ""
    monto: Decimal = Decimal("0.00")
    fecha: Optional[date] = None
    estado: EstadoPresup = EstadoPresup.PEND


@dataclass
class Interv:
    id: Optional[int] = None
    equipo: Optional[EquipoBio] = None
    equipo_id: Optional[int] = None
    solicitud: Optional[Reporte] = None
    solicitud_id: Optional[int] = None
    tipo: TipoInterv = TipoInterv.CORR
    descripcion: str = ""
    tecnico: str = ""
    fecha_ini: datetime = field(default_factory=datetime.now)
    fecha_fin: Optional[datetime] = None
    resultado: Optional[str] = None
    obs: Optional[str] = None
