from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HistoriaClinica
from .serializers import (
    CitaSerializer,
    HistoriaClinicaSerializer,
    HistoriaClinicaUpdateSerializer,
    PacienteNecesitaExamenSerializer,
    PacienteSerializer,
    PeticionPruebaSerializer,
    TriajeSerializer,
)
from .services import AtencionAmbulatoriaService

service = AtencionAmbulatoriaService()


class PacienteCreateAPIView(APIView):
    def post(self, request):
        serializer = PacienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        paciente = service.registrar_paciente(serializer.validated_data)
        return Response(PacienteSerializer(paciente).data, status=status.HTTP_201_CREATED)


class PacientePatchAPIView(APIView):
    def patch(self, request, pk):
        serializer = PacienteNecesitaExamenSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            paciente = service.actualizar_paciente_necesita_examen(
                paciente_id=pk,
                necesita_examen=serializer.validated_data.get('necesita_examen', False),
            )
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(PacienteSerializer(paciente).data, status=status.HTTP_200_OK)


class CitaListCreateAPIView(APIView):
    def get(self, request):
        citas = service.listar_citas()
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cita = service.crear_cita(serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(CitaSerializer(cita).data, status=status.HTTP_201_CREATED)


class TriajeCreateAPIView(APIView):
    def post(self, request):
        serializer = TriajeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            triaje = service.registrar_triaje(serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(TriajeSerializer(triaje).data, status=status.HTTP_201_CREATED)


class HistoriaClinicaListCreateAPIView(APIView):
    def post(self, request):
        serializer = HistoriaClinicaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            historia = service.crear_historia_clinica(serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(HistoriaClinicaSerializer(historia).data, status=status.HTTP_201_CREATED)


class HistoriaClinicaDetailAPIView(APIView):
    def patch(self, request, pk):
        try:
            historia = HistoriaClinica.objects.get(pk=pk)
        except HistoriaClinica.DoesNotExist:
            return Response({'detail': 'La historia clínica no existe.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HistoriaClinicaUpdateSerializer(historia, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            historia_actualizada = service.actualizar_historia_clinica(pk, serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(HistoriaClinicaSerializer(historia_actualizada).data, status=status.HTTP_200_OK)


class PeticionPruebaCreateAPIView(APIView):
    def post(self, request):
        serializer = PeticionPruebaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            peticion = service.crear_peticion_prueba(serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(PeticionPruebaSerializer(peticion).data, status=status.HTTP_201_CREATED)