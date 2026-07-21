from .models import Cita, HistoriaClinica, Paciente, PeticionPrueba, Triaje


class PacienteRepository:
    def create(self, numero_historia_clinica, dni, nombre_completo, fecha_nacimiento, necesita_examen=False):
        return Paciente.objects.create(
            numero_historia_clinica=numero_historia_clinica,
            dni=dni,
            nombre_completo=nombre_completo,
            fecha_nacimiento=fecha_nacimiento,
            necesita_examen=necesita_examen,
        )

    def get_by_id(self, paciente_id):
        try:
            return Paciente.objects.get(pk=paciente_id)
        except Paciente.DoesNotExist:
            return None

    def update_necesita_examen(self, paciente_id, necesita_examen):
        paciente = self.get_by_id(paciente_id)
        if not paciente:
            return None
        paciente.necesita_examen = necesita_examen
        paciente.save(update_fields=['necesita_examen'])
        return paciente


class CitaRepository:
    def create(self, paciente, fecha_hora, estado=Cita.ESTADO_PROGRAMADA):
        return Cita.objects.create(
            paciente=paciente,
            fecha_hora=fecha_hora,
            estado=estado,
        )

    def list_all(self):
        return Cita.objects.select_related('paciente').all().order_by('-fecha_hora')

    def get_by_id(self, cita_id):
        try:
            return Cita.objects.select_related('paciente').get(pk=cita_id)
        except Cita.DoesNotExist:
            return None

    def get_programada_by_paciente(self, paciente):
        return (
            Cita.objects.filter(paciente=paciente, estado=Cita.ESTADO_PROGRAMADA)
            .order_by('fecha_hora')
            .first()
        )

    def update_estado(self, cita_id, estado):
        cita = self.get_by_id(cita_id)
        if not cita:
            return None
        cita.estado = estado
        cita.save(update_fields=['estado'])
        return cita


class TriajeRepository:
    def create(self, paciente, presion_sistolica, presion_diastolica, temperatura):
        return Triaje.objects.create(
            paciente=paciente,
            presion_sistolica=presion_sistolica,
            presion_diastolica=presion_diastolica,
            temperatura=temperatura,
        )


class HistoriaClinicaRepository:
    def create(self, paciente, diagnostico=None, tratamiento=None, receta_medica=None):
        return HistoriaClinica.objects.create(
            paciente=paciente,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            receta_medica=receta_medica,
        )

    def get_by_id(self, historia_id):
        try:
            return HistoriaClinica.objects.select_related('paciente').get(pk=historia_id)
        except HistoriaClinica.DoesNotExist:
            return None

    def get_or_create_for_paciente(self, paciente):
        historia, _ = HistoriaClinica.objects.get_or_create(paciente=paciente)
        return historia

    def update(self, historia_id, **kwargs):
        historia = self.get_by_id(historia_id)
        if not historia:
            return None

        for field, value in kwargs.items():
            if value is not None:
                setattr(historia, field, value)

        historia.save()
        return historia


class PeticionPruebaRepository:
    def create(self, paciente, tipo_examen, tiene_sis):
        return PeticionPrueba.objects.create(
            paciente=paciente,
            tipo_examen=tipo_examen,
            tiene_sis=tiene_sis,
        )