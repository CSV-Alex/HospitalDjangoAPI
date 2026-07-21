from typing import List, Optional
from apps.mantenimiento_biomedico.infrastructure.models import (
    EquipoBio as EquipoBioModel,
)
from apps.mantenimiento_biomedico.domain.entities import EquipoBio
from apps.mantenimiento_biomedico.domain.repository_interfaces import IEquipoRepo
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
