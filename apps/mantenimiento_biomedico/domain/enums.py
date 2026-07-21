from enum import Enum


class TipoEquipo(str, Enum):
    DIAG = "DIAG"
    TERAPIA = "TERAPIA"
    MONIT = "MONIT"
    SOP_VIDA = "SOP_VIDA"
    LAB = "LAB"
    IMAGEN = "IMAGEN"
    OTROS = "OTROS"


class EstadoEq(str, Enum):
    OPER = "OPER"
    EN_REP = "EN_REP"
    FUERA = "FUERA"
    BAJA = "BAJA"


class EstadoRep(str, Enum):
    PEND = "PEND"
    EN_EVAL = "EN_EVAL"
    RES = "RES"
    CANC = "CANC"


class EstadoSol(str, Enum):
    PEND = "PEND"
    APR = "APR"
    RECHAZ = "RECHAZ"
    EN_PROC = "EN_PROC"


class EstadoPresup(str, Enum):
    PEND = "PEND"
    APR = "APR"
    RECHAZ = "RECHAZ"


class TipoInterv(str, Enum):
    PREV = "PREV"
    CORR = "CORR"
    CALIB = "CALIB"
