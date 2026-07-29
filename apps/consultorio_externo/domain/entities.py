import uuid
from typing import Optional
from .value_objects import (
    NumeroHistoriaClinica,
    NombreCompleto,
    FechaNacimiento,
    NecesitaExamen,
)

from .exceptions import PacienteInvalidoException


class Entity:
    
    def __init__(self, id: Optional[str] = None):
      
        self.id = id or str(uuid.uuid4())
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id!r})"


class Paciente(Entity):
    
    def __init__(
        self,
        numero_historia_clinica: NumeroHistoriaClinica,
        nombre_completo: NombreCompleto,
        fecha_nacimiento: FechaNacimiento,
        necesita_examen: NecesitaExamen,
        id: Optional[str] = None,
    ):
       
        super().__init__(id)
        
        # Validar tipos de los parámetros
        if not isinstance(numero_historia_clinica, NumeroHistoriaClinica):
            raise PacienteInvalidoException(
                f"numero_historia_clinica debe ser NumeroHistoriaClinica, "
                f"recibido: {type(numero_historia_clinica)}"
            )
        
        if not isinstance(nombre_completo, NombreCompleto):
            raise PacienteInvalidoException(
                f"nombre_completo debe ser NombreCompleto, "
                f"recibido: {type(nombre_completo)}"
            )
        
        if not isinstance(fecha_nacimiento, FechaNacimiento):
            raise PacienteInvalidoException(
                f"fecha_nacimiento debe ser FechaNacimiento, "
                f"recibido: {type(fecha_nacimiento)}"
            )
        
        if not isinstance(necesita_examen, NecesitaExamen):
            raise PacienteInvalidoException(
                f"necesita_examen debe ser NecesitaExamen, "
                f"recibido: {type(necesita_examen)}"
            )
        
        # Asignar los atributos
        self.numero_historia_clinica = numero_historia_clinica
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.necesita_examen = necesita_examen
    
    def obtener_edad(self) -> int:
        return self.fecha_nacimiento.calcular_edad()
    
    def cambiar_necesita_examen(self, nuevo_valor: NecesitaExamen) -> None:
        if not isinstance(nuevo_valor, NecesitaExamen):
            raise PacienteInvalidoException(
                f"nuevo_valor debe ser NecesitaExamen, "
                f"recibido: {type(nuevo_valor)}"
            )
        
        self.necesita_examen = nuevo_valor
    
    def __repr__(self):
        return (
            f"Paciente("
            f"id={self.id!r}, "
            f"numero_historia_clinica={self.numero_historia_clinica!r}, "
            f"nombre_completo={self.nombre_completo!r}, "
            f"fecha_nacimiento={self.fecha_nacimiento!r}, "
            f"necesita_examen={self.necesita_examen!r}"
            f")"
        )