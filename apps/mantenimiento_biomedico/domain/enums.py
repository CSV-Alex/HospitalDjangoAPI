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


class EstadoReporte(str, Enum):
    REPORTADO = "reportado"
    EVALUADO = "evaluado"
    REPARADO = "reparado"
    REEMPLAZADO = "reemplazado"
    SIN_ACCION = "sin_accion"
