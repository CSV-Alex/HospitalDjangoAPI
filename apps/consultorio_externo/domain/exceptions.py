
class DomainException(Exception):
    """Excepción base del dominio."""
    pass


class NumeroHistoriaClinicaInvalidoException(DomainException):
    """Se lanza cuando el número de historia clínica es inválido."""
    pass


class NombreCompletoInvalidoException(DomainException):
    """Se lanza cuando el nombre completo no cumple los requisitos."""
    pass


class FechaNacimientoInvalidaException(DomainException):
    """Se lanza cuando la fecha de nacimiento es inválida."""
    pass


class PacienteInvalidoException(DomainException):
    """Se lanza cuando los datos del paciente no son válidos."""
    pass


class RepositoryException(DomainException):
    """Se lanza cuando ocurre un error en el repositorio."""
    pass