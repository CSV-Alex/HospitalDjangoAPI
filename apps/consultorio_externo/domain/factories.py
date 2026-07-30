from datetime import date, datetime
from typing import Any, Dict, Union

from .entities import Paciente
from .value_objects import (
    NumeroHistoriaClinica,
    NombreCompleto,
    FechaNacimiento,
    NecesitaExamen,
)
from .exceptions import DomainException


class PacienteFactory:
    
    @staticmethod
    def crear_desde_bonita(datos: Dict[str, Any]) -> Paciente:
        try:
            # Validar que existan todas las claves requeridas
            claves_requeridas = {
                "numeroHistoriaClinica",
                "nombreCompleto",
                "fechaNacimiento",
                "necesitaExamen",
            }
            
            claves_faltantes = claves_requeridas - set(datos.keys())
            if claves_faltantes:
                raise KeyError(
                    f"Claves faltantes en los datos de Bonita: {claves_faltantes}"
                )
            
            # Extraer y procesar los datos
            numero_historia = NumeroHistoriaClinica(datos["numeroHistoriaClinica"])
            nombre = NombreCompleto(datos["nombreCompleto"])
            fecha_nacimiento = FechaNacimiento(
                PacienteFactory._procesar_fecha(datos["fechaNacimiento"])
            )
            necesita_examen = NecesitaExamen(
                PacienteFactory._procesar_booleano(datos["necesitaExamen"])
            )
            
            # Crear y retornar el Paciente
            return Paciente(
                numero_historia_clinica=numero_historia,
                nombre_completo=nombre,
                fecha_nacimiento=fecha_nacimiento,
                necesita_examen=necesita_examen,
            )
        
        except (KeyError, ValueError, DomainException) as e:
            raise DomainException(
                f"Error al crear Paciente desde datos de Bonita: {str(e)}"
            )
    
    @staticmethod
    def _procesar_fecha(valor: Union[date, datetime, str]) -> date:
        if isinstance(valor, date) and not isinstance(valor, datetime):
            return valor
        
        if isinstance(valor, datetime):
            return valor.date()
        
        if isinstance(valor, str):
            try:
                return datetime.strptime(valor, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Formato de fecha inválido: {valor}. "
                    f"Se espera formato YYYY-MM-DD"
                )
        
        raise ValueError(
            f"Tipo de fecha no soportado: {type(valor)}. "
            f"Se espera date, datetime o string (YYYY-MM-DD)"
        )
    
    @staticmethod
    def _procesar_booleano(valor: Union[bool, str, int]) -> bool:
        if isinstance(valor, bool):
            return valor
        
        if isinstance(valor, str):
            if valor.lower() in ("true", "1", "yes", "sí"):
                return True
            elif valor.lower() in ("false", "0", "no"):
                return False
            else:
                raise ValueError(
                    f"Valor string booleano no reconocido: {valor}. "
                    f"Se espera 'true', 'false', '1', '0', 'yes', 'no'"
                )
        
        if isinstance(valor, int):
            if valor == 1:
                return True
            elif valor == 0:
                return False
            else:
                raise ValueError(
                    f"Valor int booleano no reconocido: {valor}. "
                    f"Se espera 0 o 1"
                )
        
        raise ValueError(
            f"Tipo booleano no soportado: {type(valor)}. "
            f"Se espera bool, string o int"
        )