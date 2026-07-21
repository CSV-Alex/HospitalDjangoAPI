from abc import ABC, abstractmethod
from apps.mantenimiento_biomedico.domain.entities import (
    Reporte, Eval,
)


class IMantServ(ABC):

    @abstractmethod
    def rep_defecto(self, equipo_id: int, descripcion: str, reportado_por: str) -> Reporte:
        pass

    @abstractmethod
    def evaluar(self, reporte_id: int, tecnico: str, diagnostico: str, reemplazo: bool) -> Eval:
        pass


class MantServ(IMantServ):

    def __init__(self, eq_repo, rep_repo, ev_repo, sol_repo, est_repo, int_repo):
        self._eq = eq_repo
        self._rep = rep_repo
        self._ev = ev_repo
        self._sol = sol_repo
        self._est = est_repo
        self._int = int_repo

    def rep_defecto(self, equipo_id: int, descripcion: str, reportado_por: str) -> Reporte:
        eq = self._eq.find_by_id(equipo_id)
        if not eq:
            raise ValueError(f"Equipo {equipo_id} no encontrado")
        rep = self._rep.save(Reporte(equipo_id=equipo_id, descripcion=descripcion, reportado_por=reportado_por))
        eq.estado = 'EN_REP'
        self._eq.save(eq)
        return rep

    def evaluar(self, reporte_id: int, tecnico: str, diagnostico: str, reemplazo: bool) -> Eval:
        rep = self._rep.find_by_id(reporte_id)
        if not rep:
            raise ValueError(f"Reporte {reporte_id} no encontrado")
        ev = self._ev.save(Eval(reporte_id=reporte_id, tecnico=tecnico, diagnostico=diagnostico, reemplazo=reemplazo))
        rep.estado = 'EN_EVAL'
        self._rep.save(rep)
        if reemplazo:
            from apps.mantenimiento_biomedico.domain.entities import Solicitud
            self._sol.save(Solicitud(eval_id=ev.id, equipo_id=rep.equipo_id, motivo=diagnostico))
        return ev


