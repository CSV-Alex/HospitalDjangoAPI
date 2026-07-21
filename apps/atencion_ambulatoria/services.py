from .models import Cita
from .repositories import (
    CitaRepository,
    HistoriaClinicaRepository,
    PacienteRepository,
    PeticionPruebaRepository,
    TriajeRepository,
)


class AtencionAmbulatoriaService:
    def __init__(self):
        self.paciente_repo = PacienteRepository()
        self.cita_repo = CitaRepository()
        self.triaje_repo = TriajeRepository()
        self.historia_repo = HistoriaClinicaRepository()
        self.peticion_repo = PeticionPruebaRepository()

    def registrar_paciente(self, data):
        return self.paciente_repo.create(
            numero_historia_clinica=data['numero_historia_clinica'],
            dni=data['dni'],
            nombre_completo=data['nombre_completo'],
            fecha_nacimiento=data['fecha_nacimiento'],
            necesita_examen=data.get('necesita_examen', False),
        )

    def crear_cita(self, data):
        paciente = self.paciente_repo.get_by_id(data['paciente'].id if hasattr(data['paciente'], 'id') else data['paciente'])
        if not paciente:
            raise ValueError('El paciente no existe.')

        return self.cita_repo.create(
            paciente=paciente,
            fecha_hora=data['fecha_hora'],
            estado=data.get('estado', Cita.ESTADO_PROGRAMADA),
        )

    def listar_citas(self):
        return self.cita_repo.list_all()

    def registrar_triaje(self, data):
        paciente = self.paciente_repo.get_by_id(data['paciente'].id if hasattr(data['paciente'], 'id') else data['paciente'])
        if not paciente:
            raise ValueError('El paciente no existe.')

        triaje = self.triaje_repo.create(
            paciente=paciente,
            presion_sistolica=data['presion_sistolica'],
            presion_diastolica=data['presion_diastolica'],
            temperatura=data['temperatura'],
        )

        cita_programada = self.cita_repo.get_programada_by_paciente(paciente)
        if cita_programada:
            self.cita_repo.update_estado(cita_programada.id, Cita.ESTADO_EN_TRIAGE)

        return triaje

    def crear_historia_clinica(self, data):
        paciente = self.paciente_repo.get_by_id(data['paciente'].id if hasattr(data['paciente'], 'id') else data['paciente'])
        if not paciente:
            raise ValueError('El paciente no existe.')

        historia = self.historia_repo.get_or_create_for_paciente(paciente)

        if data.get('diagnostico') is not None:
            historia.diagnostico = data['diagnostico']
        if data.get('tratamiento') is not None:
            historia.tratamiento = data['tratamiento']
        if data.get('receta_medica') is not None:
            historia.receta_medica = data['receta_medica']

        historia.save()
        return historia

    def actualizar_historia_clinica(self, historia_id, data):
        historia = self.historia_repo.update(
            historia_id,
            diagnostico=data.get('diagnostico'),
            tratamiento=data.get('tratamiento'),
            receta_medica=data.get('receta_medica'),
        )
        if not historia:
            raise ValueError('La historia clínica no existe.')

        cita_en_triage = self.cita_repo.get_programada_by_paciente(historia.paciente)
        if cita_en_triage:
            self.cita_repo.update_estado(cita_en_triage.id, Cita.ESTADO_EN_CONSULTA)

        return historia

    def actualizar_paciente_necesita_examen(self, paciente_id, necesita_examen):
        paciente = self.paciente_repo.update_necesita_examen(paciente_id, necesita_examen)
        if not paciente:
            raise ValueError('El paciente no existe.')
        return paciente

    def crear_peticion_prueba(self, data):
        paciente = self.paciente_repo.get_by_id(data['paciente'].id if hasattr(data['paciente'], 'id') else data['paciente'])
        if not paciente:
            raise ValueError('El paciente no existe.')

        paciente.necesita_examen = True
        paciente.save(update_fields=['necesita_examen'])

        return self.peticion_repo.create(
            paciente=paciente,
            tipo_examen=data['tipo_examen'],
            tiene_sis=data['tiene_sis'],
        )