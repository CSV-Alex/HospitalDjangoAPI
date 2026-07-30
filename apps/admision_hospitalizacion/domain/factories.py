from typing import Dict, Any
from .entities import HospitalizacionRequest
from .value_objects import NumeroOrden, DniPaciente, Especialidad, CodigoCama
from .exceptions import ValidacionException

class HospitalizacionFactory:
    """Factory para crear entidades de HospitalizacionRequest desde diferentes fuentes."""
    
    @staticmethod
    def crear_desde_bonita(datos: Dict[str, Any]) -> HospitalizacionRequest:
        try:
            numero_orden = NumeroOrden(str(datos.get('numeroOrden', '')))
            dni_paciente = DniPaciente(str(datos.get('dniPaciente', '')))
            especialidad = Especialidad(str(datos.get('especialidad', '')))
            codigo_cama = CodigoCama(str(datos.get('codigoCama', '')))
            
            return HospitalizacionRequest(
                numero_orden=numero_orden,
                dni_paciente=dni_paciente,
                especialidad=especialidad,
                codigo_cama=codigo_cama
            )
        except ValidacionException as e:
            # Re-lanzamos la excepción de dominio si hay error de validación
            raise
        except Exception as e:
            raise ValidacionException(f"Error al construir la solicitud de hospitalización: {str(e)}")
