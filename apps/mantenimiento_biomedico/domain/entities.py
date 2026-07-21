from dataclasses import dataclass
from datetime import date
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
