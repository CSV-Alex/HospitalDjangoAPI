import logging
from typing import Dict, Any, Optional

from apps.mantenimiento_biomedico.domain.entities import Reporte
from apps.mantenimiento_biomedico.domain.enums import EstadoReporte
from apps.mantenimiento_biomedico.infrastructure.repositories import ReporteRepo

logger = logging.getLogger(__name__)


class ProcesarReporteService:

    def __init__(self, repo: Optional[ReporteRepo] = None):
        self.repo = repo or ReporteRepo()

    def procesar(self, datos: Dict[str, Any]) -> Reporte:
        external_id = datos.get('reporteId')
        descripcion = datos.get('descripcionFalla', '')
        requiere_reparacion = datos.get('requiereReparacion', True)
        reparacion_exitosa = datos.get('reparacionExitosa', True)

        existente = self.repo.find_by_external_id(external_id) if external_id else None

        if existente:
            print(f"Actualizando reporte #{existente.id} "
                  f"(requiereReparacion={requiere_reparacion}, "
                  f"reparacionExitosa={reparacion_exitosa})")
            return self._actualizar(existente, requiere_reparacion, reparacion_exitosa)

        print(f"Creando reporte (external_id={external_id})")
        return self._crear(external_id, descripcion, requiere_reparacion, reparacion_exitosa)

    def _crear(self, external_id: Optional[str], descripcion: str,
               requiere_reparacion: bool, reparacion_exitosa: bool) -> Reporte:
        reporte = Reporte(
            equipo_id=None,
            descripcion_falla=descripcion,
            estado=EstadoReporte.REPORTADO,
            isRepairable=requiere_reparacion,
            repairSuccessful=reparacion_exitosa,
            external_id=external_id,
        )
        return self.repo.save(reporte)

    def _actualizar(self, existente: Reporte,
                    requiere_reparacion: bool, reparacion_exitosa: bool) -> Reporte:
        actualizado = Reporte(
            id=existente.id,
            equipo_id=existente.equipo_id,
            equipo_codigo=existente.equipo_codigo,
            equipo_nombre=existente.equipo_nombre,
            descripcion_falla=existente.descripcion_falla,
            fecha_reporte=existente.fecha_reporte,
            isEvaluated=existente.isEvaluated,
            isRepairable=existente.isRepairable if requiere_reparacion else False,
            repairSuccessful=existente.repairSuccessful if reparacion_exitosa else False,
            external_id=existente.external_id,
            estado=existente.estado,
        )
        return self.repo.save(actualizado)
