from enum import Enum


class EstadoCampana(str, Enum):
    PLANIF = "PLANIF"
    EN_CURSO = "EN_CURSO"
    SUSP = "SUSP"
    FINALIZ = "FINALIZ"


class TipoVacuna(str, Enum):
    ARN = "ARN"
    VIRAL = "VIRAL"
    BACTERIANA = "BACTERIANA"
    TOXOIDE = "TOXOIDE"
    VIVA = "VIVA"
    INACTIVADA = "INACTIVADA"
    OTROS = "OTROS"


class EstadoLote(str, Enum):
    DISP = "DISP"
    EN_USO = "EN_USO"
    AGOTADO = "AGOTADO"
    VENCIDO = "VENCIDO"


class EstadoRegistro(str, Enum):
    PEND = "PEND"
    COMPLETO = "COMPLETO"
    REACCADV = "REACCADV"
    CONTRAINDICADO = "CONTRAINDICADO"
