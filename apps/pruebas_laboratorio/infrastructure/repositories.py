from typing import List, Optional
from apps.pruebas_laboratorio.infrastructure.models import (
    Paciente as PacienteModel,
    SolicitudPrueba as SolicitudPruebaModel,
    ResultadoPrueba as ResultadoPruebaModel
)
from apps.pruebas_laboratorio.domain.entities import (
    Paciente, SolicitudPrueba, ResultadoPrueba
)
from apps.pruebas_laboratorio.domain.repository_interface import (
    IPacienteRepo, ISolicitudPruebaRepo, IResultadoPruebaRepo
)

class PacienteRepo(IPacienteRepo):

    @staticmethod
    def _to_entity(m: PacienteModel) -> Paciente:
        return Paciente(
            id=m.id, nombre=m.nombre,
            apellido=m.apellido, fecha_nac=m.fecha_nac,
            sexo=m.sexo, direccion=m.direccion,
            telefono=m.telefono
        )

    def save(self, eq: Paciente) -> Paciente:
        m = PacienteModel.objects.get(id=eq.id) if eq.id else PacienteModel()
        m.nombre = eq.nombre
        m.apellido = eq.apellido
        m.fecha_nac = eq.fecha_nac
        m.sexo = eq.sexo
        m.direccion = eq.direccion
        m.telefono = eq.telefono
        m.save()
        return self._to_entity(m)

    def find_by_id(self, eq_id: int) -> Optional[Paciente]:
        try:
            return self._to_entity(PacienteModel.objects.get(id=eq_id))
        except PacienteModel.DoesNotExist:
            return None

    def find_all(self) -> List[Paciente]:
        return [self._to_entity(m) for m in PacienteModel.objects.all()]

    def delete(self, eq_id: int) -> None:
        PacienteModel.objects.filter(id=eq_id).delete()


class SolicitudPruebaRepo(ISolicitudPruebaRepo):

    @staticmethod
    def _to_entity(m: SolicitudPruebaModel) -> SolicitudPrueba:
        return SolicitudPrueba(
            id=m.id, paciente_id=m.paciente_id,
            tipo_prueba=m.tipo_prueba, fecha_solicitud=m.fecha_solicitud,
            estado=m.estado
        )

    def save(self, r: SolicitudPrueba) -> SolicitudPrueba:
        m = SolicitudPruebaModel.objects.get(id=r.id) if r.id else SolicitudPruebaModel()
        m.paciente_id = r.paciente_id
        m.tipo_prueba = r.tipo_prueba
        m.estado = r.estado
        return self._to_entity(m)

    def find_by_id(self, r_id: int) -> Optional[SolicitudPrueba]:
        try:
            return self._to_entity(SolicitudPruebaModel.objects.get(id=r_id))
        except SolicitudPruebaModel.DoesNotExist:
            return None

    def find_all(self) -> List[SolicitudPrueba]:
        return [self._to_entity(m) for m in SolicitudPruebaModel.objects.all()]

    def delete(self, r_id: int) -> None:
        SolicitudPruebaModel.objects.filter(id=r_id).delete()


class ResultadoPruebaRepo(IResultadoPruebaRepo):

    @staticmethod
    def _to_entity(m: ResultadoPruebaModel) -> ResultadoPrueba:
        return ResultadoPrueba(
            id=m.id, solicitud_id=m.solicitud_id,
            resultado=m.resultado, fecha_resultado=m.fecha_resultado
        )

    def save(self, ev: ResultadoPrueba) -> ResultadoPrueba:
        m = ResultadoPruebaModel.objects.get(id=ev.id) if ev.id else ResultadoPruebaModel()
        m.solicitud_id = ev.solicitud_id
        m.resultado = ev.resultado
        m.save()
        return self._to_entity(m)

    def find_by_id(self, ev_id: int) -> Optional[ResultadoPrueba]:
        try:
            return self._to_entity(ResultadoPruebaModel.objects.get(id=ev_id))
        except ResultadoPruebaModel.DoesNotExist:
            return None

    def find_all(self) -> List[ResultadoPrueba]:
        return [self._to_entity(m) for m in ResultadoPruebaModel.objects.all()]

    def delete(self, ev_id: int) -> None:
        ResultadoPruebaModel.objects.filter(id=ev_id).delete()