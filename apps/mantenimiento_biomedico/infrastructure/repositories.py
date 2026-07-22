from typing import List, Optional
from apps.mantenimiento_biomedico.infrastructure.models import (
    EquipoBio as EquipoBioModel,
    Reporte as ReporteModel,
)
from apps.mantenimiento_biomedico.domain.entities import EquipoBio, Reporte
from apps.mantenimiento_biomedico.domain.repository_interfaces import IEquipoRepo, IReporteRepo
from apps.mantenimiento_biomedico.domain.enums import (
    TipoEquipo, EstadoEq,
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

    def find_by_codigo(self, codigo: str) -> Optional[EquipoBio]:
        try:
            return self._to_entity(EquipoBioModel.objects.get(codigo=codigo))
        except EquipoBioModel.DoesNotExist:
            return None


class ReporteRepo(IReporteRepo):

    @staticmethod
    def _to_entity(m: ReporteModel) -> Reporte:
        return Reporte(
            id=m.id, equipo_id=m.equipo_id,
            equipo_codigo=m.equipo.codigo,
            equipo_nombre=m.equipo.nombre,
            descripcion_falla=m.descripcion_falla,
            fecha_reporte=m.fecha_reporte,
            isEvaluated=m.isEvaluated,
            isRepairable=m.isRepairable,
        )

    def save(self, r: Reporte) -> Reporte:
        m = ReporteModel.objects.get(id=r.id) if r.id else ReporteModel()
        m.equipo_id = r.equipo_id
        m.descripcion_falla = r.descripcion_falla
        m.isEvaluated = r.isEvaluated
        m.isRepairable = r.isRepairable
        m.save()
        return self._to_entity(m)

    def find_by_id(self, r_id: int) -> Optional[Reporte]:
        try:
            return self._to_entity(ReporteModel.objects.select_related('equipo').get(id=r_id))
        except ReporteModel.DoesNotExist:
            return None

    def find_all(self) -> List[Reporte]:
        return [
            self._to_entity(m)
            for m in ReporteModel.objects.select_related('equipo').all()
        ]

    def delete(self, r_id: int) -> None:
        ReporteModel.objects.filter(id=r_id).delete()
