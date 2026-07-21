from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Paciente:
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    fecha_nac: Optional[date] = None
    sexo: str = ""
    direccion: str = ""
    telefono: str = ""

@dataclass
class SolicitudPrueba:
    id: Optional[int] = None
    paciente: Optional[Paciente] = None
    tipo_prueba: str = ""
    fecha_solicitud: datetime = field(default_factory=datetime.now)
    estado: str = "Pendiente"

@dataclass
class ResultadoPrueba:
    id: Optional[int] = None
    solicitud: Optional[SolicitudPrueba] = None
    resultado: str = ""
    fecha_resultado: datetime = field(default_factory=datetime.now)

