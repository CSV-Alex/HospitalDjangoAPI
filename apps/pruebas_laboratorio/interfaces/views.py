from datetime import date
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# wfrom apps.mantenimiento_biomedico.application.services import MantServ
from apps.pruebas_laboratorio.infrastructure.repositories import (
    PacienteRepo, SolicitudPruebaRepo, ResultadoPruebaRepo,
)
from apps.pruebas_laboratorio.interfaces.serializers import (
    PacienteSer, SolicitudPruebaSer, ResultadoPruebaSer,
)

_pac_repo = PacienteRepo()
_sol_repo = SolicitudPruebaRepo()
_res_repo = ResultadoPruebaRepo()


class PacienteView(APIView):

    def get(self, request, pk=None):
        if pk:
            p = _pac_repo.find_by_id(pk)
            return Response(PacienteSer(p).data) if p else Response({"error": "no encontrado"}, status=404)
        return Response([PacienteSer(p).data for p in _pac_repo.find_all()])

    def post(self, request):
        p = _pac_repo.save(PacienteSer(data=request.data).create())
        return Response(PacienteSer(p).data, status=201)


class SolicitudPruebaView(APIView):

    def get(self, request, pk=None):
        if pk:
            s = _sol_repo.find_by_id(pk)
            return Response(SolicitudPruebaSer(s).data) if s else Response({"error": "no encontrado"}, status=404)
        return Response([SolicitudPruebaSer(s).data for s in _sol_repo.find_all()])

    def post(self, request):
        s = _sol_repo.save(SolicitudPruebaSer(data=request.data).create())
        return Response(SolicitudPruebaSer(s).data, status=201)
    

class ResultadoPruebaView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            r = _res_repo.find_by_id(pk)
            return Response(ResultadoPruebaSer(r).data) if r else Response({"error": "no encontrado"}, status=404)
        return Response([ResultadoPruebaSer(r).data for r in _res_repo.find_all()])

    def post(self, request):
        r = _res_repo.save(ResultadoPruebaSer(data=request.data).create())
        return Response(ResultadoPruebaSer(r).data, status=201)