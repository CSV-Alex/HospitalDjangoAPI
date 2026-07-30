from typing import Optional
from .value_objects import NumeroOrden, DniPaciente, Especialidad, CodigoCama

class HospitalizacionRequest:
    """Entidad de dominio que representa la solicitud de hospitalización."""
    
    def __init__(
        self,
        numero_orden: NumeroOrden,
        dni_paciente: DniPaciente,
        especialidad: Especialidad,
        codigo_cama: CodigoCama
    ):
        self.numero_orden = numero_orden
        self.dni_paciente = dni_paciente
        self.especialidad = especialidad
        self.codigo_cama = codigo_cama

    def __str__(self):
        return (f"HospitalizacionRequest(Orden: {self.numero_orden.valor}, "
                f"DNI: {self.dni_paciente.valor}, Cama: {self.codigo_cama.valor})")
