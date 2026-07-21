from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

class PacienteRepository:
    @staticmethod
    def get_by_dni(dni):
        return Paciente.objects.filter(dni=dni).first()

    @staticmethod
    def create(data):
        return Paciente.objects.create(**data)

class CamaRepository:
    @staticmethod
    def find_available_by_specialty(especialidad):
        return Cama.objects.filter(especialidad=especialidad, disponible=True).first()

    @staticmethod
    def update_disponibilidad(cama, disponible):
        cama.disponible = disponible
        cama.save()
        return cama

class OrdenInternamientoRepository:
    @staticmethod
    def create(data):
        return OrdenInternamiento.objects.create(**data)

    @staticmethod
    def get_by_id(orden_id):
        return OrdenInternamiento.objects.filter(id=orden_id).first()

    @staticmethod
    def update_estado(orden, estado):
        orden.estado = estado
        orden.save()
        return orden

class HospitalizacionRepository:
    @staticmethod
    def create(data):
        return Hospitalizacion.objects.create(**data)

    @staticmethod
    def get_by_orden(orden):
        return Hospitalizacion.objects.filter(orden=orden).first()

class HistoriaClinicaRepository:
    @staticmethod
    def create(data):
        return HistoriaClinica.objects.create(**data)
