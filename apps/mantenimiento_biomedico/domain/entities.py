from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from apps.mantenimiento_biomedico.domain.enums import (
    TipoEquipo, EstadoEq,
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
    equipo_id: Optional[int] = None
    equipo_codigo: str = ""
    equipo_nombre: str = ""
    descripcion_falla: str = ""
    fecha_reporte: Optional[datetime] = None
