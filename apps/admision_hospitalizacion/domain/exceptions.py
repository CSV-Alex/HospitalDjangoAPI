class DomainException(Exception):
    """Excepción base para errores de dominio."""
    pass

class PacienteNoEncontradoException(DomainException):
    def __init__(self, dni: str):
        super().__init__(f"Paciente con DNI {dni} no encontrado")

class CamaNoDisponibleException(DomainException):
    def __init__(self, codigo_cama: str):
        super().__init__(f"Cama {codigo_cama} no disponible o no encontrada")

class ValidacionException(DomainException):
    """Excepción para errores de validación de datos."""
    pass
