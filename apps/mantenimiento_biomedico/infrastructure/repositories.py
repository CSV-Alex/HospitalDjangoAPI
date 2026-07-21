from typing import List, Optional
from apps.mantenimiento_biomedico.infrastructure.models import (
    EquipoBio as EquipoBioModel,
    Reporte as ReporteModel,
    Eval as EvalModel,
    Solicitud as SolicitudModel,
    Estimacion as EstimacionModel,
    Interv as IntervModel,
)
from apps.mantenimiento_biomedico.domain.entities import (
    EquipoBio, Reporte, Eval,
    Solicitud, Estimacion, Interv,
)
from apps.mantenimiento_biomedico.domain.repository_interfaces import (
    IEquipoRepo, IReporteRepo,
    IEvalRepo, ISolicitudRepo,
    IEstimacionRepo, IIntervRepo,
)
from apps.mantenimiento_biomedico.domain.enums import (
    TipoEquipo, EstadoEq, EstadoRep,
    EstadoSol, TipoInterv,
)


class EquipoRepo(IEquipoRepo):

    @staticmethod
    def _to_entity(m: EquipoBioModel) -> EquipoBio:
        return EquipoBio(
            id=m.id, codigo=m.codigo, nombre=m.nombre,
            tipo=TipoEquipo(m.tipo), fabricante=m.fabricante,
            modelo=m.modelo, num_serie=m.num_serie,
            ubicacion=m.ubicacion, fecha_adq=m.fecha_adq,
            fecha_ult_calib=m.fecha_ult_calib, estado=EstadoEq(m.estado),
        )

    def save(self, eq: EquipoBio) -> EquipoBio:
        m = EquipoBioModel.objects.get(id=eq.id) if eq.id else EquipoBioModel()
        m.codigo = eq.codigo
        m.nombre = eq.nombre
        m.tipo = eq.tipo.value
        m.fabricante = eq.fabricante
        m.modelo = eq.modelo
        m.num_serie = eq.num_serie
        m.ubicacion = eq.ubicacion
        m.fecha_adq = eq.fecha_adq
        m.fecha_ult_calib = eq.fecha_ult_calib
        m.estado = eq.estado.value
        m.save()
        return self._to_entity(m)

    def find_by_id(self, eq_id: int) -> Optional[EquipoBio]:
        try:
            return self._to_entity(EquipoBioModel.objects.get(id=eq_id))
        except EquipoBioModel.DoesNotExist:
            return None

    def find_all(self) -> List[EquipoBio]:
        return [self._to_entity(m) for m in EquipoBioModel.objects.all()]

    def delete(self, eq_id: int) -> None:
        EquipoBioModel.objects.filter(id=eq_id).delete()


class ReporteRepo(IReporteRepo):

    @staticmethod
    def _to_entity(m: ReporteModel) -> Reporte:
        return Reporte(
            id=m.id, equipo_id=m.equipo_id,
            descripcion=m.descripcion, reportado_por=m.reportado_por,
            fecha=m.fecha, estado=EstadoRep(m.estado),
        )

    def save(self, r: Reporte) -> Reporte:
        m = ReporteModel.objects.get(id=r.id) if r.id else ReporteModel()
        m.equipo_id = r.equipo_id
        m.descripcion = r.descripcion
        m.reportado_por = r.reportado_por
        m.estado = r.estado.value
        m.save()
        return self._to_entity(m)

    def find_by_id(self, r_id: int) -> Optional[Reporte]:
        try:
            return self._to_entity(ReporteModel.objects.get(id=r_id))
        except ReporteModel.DoesNotExist:
            return None

    def find_all(self) -> List[Reporte]:
        return [self._to_entity(m) for m in ReporteModel.objects.all()]

    def delete(self, r_id: int) -> None:
        ReporteModel.objects.filter(id=r_id).delete()


class EvalRepo(IEvalRepo):

    @staticmethod
    def _to_entity(m: EvalModel) -> Eval:
        return Eval(
            id=m.id, reporte_id=m.reporte_id,
            tecnico=m.tecnico, diagnostico=m.diagnostico,
            reemplazo=m.reemplazo, fecha=m.fecha,
        )

    def save(self, ev: Eval) -> Eval:
        m = EvalModel.objects.get(id=ev.id) if ev.id else EvalModel()
        m.reporte_id = ev.reporte_id
        m.tecnico = ev.tecnico
        m.diagnostico = ev.diagnostico
        m.reemplazo = ev.reemplazo
        m.save()
        return self._to_entity(m)

    def find_by_id(self, ev_id: int) -> Optional[Eval]:
        try:
            return self._to_entity(EvalModel.objects.get(id=ev_id))
        except EvalModel.DoesNotExist:
            return None

    def find_all(self) -> List[Eval]:
        return [self._to_entity(m) for m in EvalModel.objects.all()]


class SolicitudRepo(ISolicitudRepo):

    @staticmethod
    def _to_entity(m: SolicitudModel) -> Solicitud:
        return Solicitud(
            id=m.id, eval_id=m.eval_id,
            equipo_id=m.equipo_id, motivo=m.motivo,
            fecha=m.fecha, estado=EstadoSol(m.estado),
        )

    def save(self, sol: Solicitud) -> Solicitud:
        m = SolicitudModel.objects.get(id=sol.id) if sol.id else SolicitudModel()
        m.eval_id = sol.eval_id
        m.equipo_id = sol.equipo_id
        m.motivo = sol.motivo
        m.estado = sol.estado.value
        m.save()
        return self._to_entity(m)

    def find_by_id(self, sol_id: int) -> Optional[Solicitud]:
        try:
            return self._to_entity(SolicitudModel.objects.get(id=sol_id))
        except SolicitudModel.DoesNotExist:
            return None

    def find_all(self) -> List[Solicitud]:
        return [self._to_entity(m) for m in SolicitudModel.objects.all()]


class EstimacionRepo(IEstimacionRepo):

    @staticmethod
    def _to_entity(m: EstimacionModel) -> Estimacion:
        return Estimacion(
            id=m.id, solicitud_id=m.solicitud_id,
            precio=m.precio, proveedor=m.proveedor,
            detalle=m.detalle, fecha=m.fecha,
        )

    def save(self, est: Estimacion) -> Estimacion:
        m = EstimacionModel.objects.get(id=est.id) if est.id else EstimacionModel()
        m.solicitud_id = est.solicitud_id
        m.precio = est.precio
        m.proveedor = est.proveedor
        m.detalle = est.detalle
        m.save()
        return self._to_entity(m)

    def find_by_id(self, est_id: int) -> Optional[Estimacion]:
        try:
            return self._to_entity(EstimacionModel.objects.get(id=est_id))
        except EstimacionModel.DoesNotExist:
            return None

    def find_all(self) -> List[Estimacion]:
        return [self._to_entity(m) for m in EstimacionModel.objects.all()]


class IntervRepo(IIntervRepo):

    @staticmethod
    def _to_entity(m: IntervModel) -> Interv:
        return Interv(
            id=m.id, equipo_id=m.equipo_id,
            solicitud_id=m.solicitud_id, tipo=TipoInterv(m.tipo),
            descripcion=m.descripcion, tecnico=m.tecnico,
            fecha_ini=m.fecha_ini, fecha_fin=m.fecha_fin,
            resultado=m.resultado, obs=m.obs,
        )

    def save(self, it: Interv) -> Interv:
        m = IntervModel.objects.get(id=it.id) if it.id else IntervModel()
        m.equipo_id = it.equipo_id
        m.solicitud_id = it.solicitud_id
        m.tipo = it.tipo.value
        m.descripcion = it.descripcion
        m.tecnico = it.tecnico
        m.fecha_fin = it.fecha_fin
        m.resultado = it.resultado
        m.obs = it.obs
        m.save()
        return self._to_entity(m)

    def find_by_id(self, it_id: int) -> Optional[Interv]:
        try:
            return self._to_entity(IntervModel.objects.get(id=it_id))
        except IntervModel.DoesNotExist:
            return None

    def find_by_equipo_id(self, eq_id: int) -> List[Interv]:
        return [self._to_entity(m) for m in IntervModel.objects.filter(equipo_id=eq_id)]

    def find_all(self) -> List[Interv]:
        return [self._to_entity(m) for m in IntervModel.objects.all()]
