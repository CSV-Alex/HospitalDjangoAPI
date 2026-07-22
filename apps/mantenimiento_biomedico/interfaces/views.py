from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.mantenimiento_biomedico.infrastructure.repositories import EquipoRepo, ReporteRepo
from apps.mantenimiento_biomedico.interfaces.serializers import EquipoSer, ReporteSer


_repo = EquipoRepo()
_reporte_repo = ReporteRepo()


class EquipoView(APIView):

    def get(self, request, pk=None):
        if pk:
            eq = _repo.find_by_id(pk)
            if not eq:
                return Response({"error": "Equipo no encontrado"}, status=404)
            return Response(EquipoSer(eq).data)
        return Response([EquipoSer(e).data for e in _repo.find_all()])

    def post(self, request):
        from apps.mantenimiento_biomedico.domain.entities import EquipoBio
        from apps.mantenimiento_biomedico.domain.enums import EstadoEq, TipoEquipo

        codigo = request.data.get('codigo')
        if not codigo:
            return Response({"error": "El campo 'codigo' es requerido"}, status=400)

        if _repo.find_by_codigo(codigo):
            return Response(
                {"error": f"Ya existe un equipo con el código '{codigo}'"},
                status=409,
            )

        nombre = request.data.get('nombre')
        if not nombre:
            return Response({"error": "El campo 'nombre' es requerido"}, status=400)

        tipo_str = request.data.get('tipo', 'OTROS')
        try:
            tipo = TipoEquipo(tipo_str)
        except ValueError:
            validos = [e.value for e in TipoEquipo]
            return Response(
                {"error": f"Tipo inválido '{tipo_str}'. Válidos: {', '.join(validos)}"},
                status=400,
            )

        eq = EquipoBio(
            codigo=codigo, nombre=nombre, tipo=tipo,
            fabricante=request.data.get('fabricante', ''),
            modelo=request.data.get('modelo', ''),
            num_serie=request.data.get('num_serie', ''),
            ubicacion=request.data.get('ubicacion', ''),
            estado=EstadoEq.OPER,
        )
        try:
            saved = _repo.save(eq)
            return Response(EquipoSer(saved).data, status=201)
        except Exception as e:
            return Response({"error": f"Error al guardar: {str(e)}"}, status=500)

    def delete(self, request, pk):
        eq = _repo.find_by_id(pk)
        if not eq:
            return Response({"error": "Equipo no encontrado"}, status=404)
        _repo.delete(pk)
        return Response(status=204)


class ReporteView(APIView):

    def get(self, request, pk=None):
        if pk:
            r = _reporte_repo.find_by_id(pk)
            if not r:
                return Response({"error": "Reporte no encontrado"}, status=404)
            return Response(ReporteSer(r).data)
        return Response([ReporteSer(r).data for r in _reporte_repo.find_all()])

    def post(self, request):
        from apps.mantenimiento_biomedico.domain.entities import Reporte

        equipo_id = request.data.get('equipo_id')
        if not equipo_id:
            return Response({"error": "El campo 'equipo_id' es requerido"}, status=400)

        if not _repo.find_by_id(equipo_id):
            return Response({"error": f"No existe equipo con id '{equipo_id}'"}, status=404)

        descripcion_falla = request.data.get('descripcion_falla')
        if not descripcion_falla:
            return Response({"error": "El campo 'descripcion_falla' es requerido"}, status=400)

        r = Reporte(
            equipo_id=equipo_id,
            descripcion_falla=descripcion_falla,
        )
        try:
            saved = _reporte_repo.save(r)
            return Response(ReporteSer(saved).data, status=201)
        except Exception as e:
            return Response({"error": f"Error al guardar: {str(e)}"}, status=500)

    def delete(self, request, pk):
        r = _reporte_repo.find_by_id(pk)
        if not r:
            return Response({"error": "Reporte no encontrado"}, status=404)
        _reporte_repo.delete(pk)
        return Response(status=204)


class EvaluarView(APIView):

    def patch(self, request, pk):
        from apps.mantenimiento_biomedico.domain.entities import Reporte

        r = _reporte_repo.find_by_id(pk)
        if not r:
            return Response({"error": "Reporte no encontrado"}, status=404)

        isRepairable = request.data.get('isRepairable')
        if isRepairable is None:
            return Response({"error": "El campo 'isRepairable' es requerido"}, status=400)

        if not isinstance(isRepairable, bool):
            return Response({"error": "El campo 'isRepairable' debe ser un booleano"}, status=400)

        updated = Reporte(
            id=r.id, equipo_id=r.equipo_id,
            equipo_codigo=r.equipo_codigo, equipo_nombre=r.equipo_nombre,
            descripcion_falla=r.descripcion_falla, fecha_reporte=r.fecha_reporte,
            isEvaluated=True, isRepairable=isRepairable,
        )
        saved = _reporte_repo.save(updated)
        return Response(ReporteSer(saved).data)


class RepararView(APIView):

    def patch(self, request, pk):
        r = _reporte_repo.find_by_id(pk)
        if not r:
            return Response({"error": "Reporte no encontrado"}, status=404)

        if not r.isEvaluated:
            return Response({"error": "El reporte debe ser evaluado primero"}, status=400)

        if not r.isRepairable:
            return Response({"error": "El reporte no es reparable, no se puede reparar"}, status=400)

        return Response({"mensaje": "Reparación completada exitosamente"})
