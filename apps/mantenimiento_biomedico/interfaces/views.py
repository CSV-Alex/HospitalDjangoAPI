from datetime import date
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.mantenimiento_biomedico.application.services import MantServ
from apps.mantenimiento_biomedico.infrastructure.repositories import (
    EquipoRepo, ReporteRepo, EvalRepo, SolicitudRepo,
    EstimacionRepo, IntervRepo,
)
from apps.mantenimiento_biomedico.interfaces.serializers import (
    EquipoSer, ReporteSer, EvalSer, SolicitudSer,
    EstimacionSer, IntervSer,
)


_svc = MantServ(
    eq_repo=EquipoRepo(), rep_repo=ReporteRepo(), ev_repo=EvalRepo(),
    sol_repo=SolicitudRepo(), est_repo=EstimacionRepo(),
    int_repo=IntervRepo(),
)
_eq_repo = EquipoRepo()
_rep_repo = ReporteRepo()
_ev_repo = EvalRepo()
_sol_repo = SolicitudRepo()
_est_repo = EstimacionRepo()
_int_repo = IntervRepo()


class EquipoView(APIView):

    def get(self, request, pk=None):
        if pk:
            eq = _eq_repo.find_by_id(pk)
            return Response(EquipoSer(eq).data) if eq else Response({"error": "no encontrado"}, status=404)
        return Response([EquipoSer(e).data for e in _eq_repo.find_all()])

    def post(self, request):
        from apps.mantenimiento_biomedico.domain.entities import EquipoBio
        from apps.mantenimiento_biomedico.domain.enums import EstadoEq, TipoEquipo
        tipo_req = request.data.get('tipo', 'OTROS')
        if isinstance(tipo_req, str):
            tipo_req = TipoEquipo(tipo_req)
        eq = EquipoBio(
            codigo=request.data['codigo'], nombre=request.data['nombre'],
            tipo=tipo_req, fabricante=request.data.get('fabricante', ''),
            modelo=request.data.get('modelo', ''),
            num_serie=request.data.get('num_serie', ''),
            ubicacion=request.data.get('ubicacion', ''),
            estado=EstadoEq.OPER,
        )
        return Response(EquipoSer(_eq_repo.save(eq)).data, status=201)

    def delete(self, request, pk):
        _eq_repo.delete(pk)
        return Response(status=204)


class ReporteView(APIView):

    def get(self, request, pk=None):
        if pk:
            r = _rep_repo.find_by_id(pk)
            return Response(ReporteSer(r).data) if r else Response({"error": "no encontrado"}, status=404)
        return Response([ReporteSer(r).data for r in _rep_repo.find_all()])


class EvalView(APIView):

    def get(self, request, pk=None):
        if pk:
            e = _ev_repo.find_by_id(pk)
            return Response(EvalSer(e).data) if e else Response({"error": "no encontrado"}, status=404)
        return Response([EvalSer(e).data for e in _ev_repo.find_all()])


class SolicitudView(APIView):

    def get(self, request, pk=None):
        if pk:
            s = _sol_repo.find_by_id(pk)
            return Response(SolicitudSer(s).data) if s else Response({"error": "no encontrado"}, status=404)
        return Response([SolicitudSer(s).data for s in _sol_repo.find_all()])


class EstimacionView(APIView):

    def get(self, request, pk=None):
        if pk:
            e = _est_repo.find_by_id(pk)
            return Response(EstimacionSer(e).data) if e else Response({"error": "no encontrado"}, status=404)
        return Response([EstimacionSer(e).data for e in _est_repo.find_all()])

    def post(self, request):
        from apps.mantenimiento_biomedico.domain.entities import Estimacion
        e = Estimacion(
            solicitud_id=request.data['solicitud_id'],
            precio=Decimal(str(request.data['precio'])),
            proveedor=request.data.get('proveedor', ''),
            detalle=request.data.get('detalle', ''),
        )
        return Response(EstimacionSer(_est_repo.save(e)).data, status=201)


class IntervView(APIView):

    def get(self, request):
        return Response([IntervSer(i).data for i in _int_repo.find_all()])


class CalibView(APIView):

    def post(self, request, pk):
        eq = _eq_repo.find_by_id(pk)
        if not eq:
            return Response({"error": "no encontrado"}, status=404)
        from apps.mantenimiento_biomedico.domain.entities import Interv
        from apps.mantenimiento_biomedico.domain.enums import TipoInterv
        it = _int_repo.save(Interv(
            equipo_id=pk, tipo=TipoInterv.CALIB,
            descripcion=request.data.get('descripcion', ''),
            tecnico=request.data.get('tecnico', ''),
            resultado=request.data.get('resultado', ''),
        ))
        eq.fecha_ult_calib = date.today()
        _eq_repo.save(eq)
        return Response(IntervSer(it).data, status=201)


class HistIntervView(APIView):

    def get(self, request, pk):
        return Response([IntervSer(i).data for i in _int_repo.find_by_equipo_id(pk)])


class RepDefectoView(APIView):

    def post(self, request):
        try:
            rep = _svc.rep_defecto(
                equipo_id=request.data['equipo_id'],
                descripcion=request.data['descripcion'],
                reportado_por=request.data['reportado_por'],
            )
            return Response(ReporteSer(rep).data, status=201)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class EvalBPMView(APIView):

    def post(self, request):
        try:
            ev = _svc.evaluar(
                reporte_id=request.data['reporte_id'],
                tecnico=request.data['tecnico'],
                diagnostico=request.data['diagnostico'],
                reemplazo=request.data.get('reemplazo', False),
            )
            return Response(EvalSer(ev).data, status=201)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)



