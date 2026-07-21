from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from apps.mantenimiento_biomedico.domain.enums import ()

@dataclass
class Paciente:
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    fecha_nac: Optional[date] = None
    sexo: str = ""
    direccion: str = ""
    telefono: str = ""
    email: str = ""