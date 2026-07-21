from django.core.exceptions import ValidationError
from .repositories import (
    PacienteRepository, CamaRepository, OrdenInternamientoRepository,
    HospitalizacionRepository, HistoriaClinicaRepository
)

class AdmisionService:

    @staticmethod
    def recepcionar_orden(data):
        paciente = PacienteRepository.get_by_dni(data['dni'])
        if not paciente:
            paciente = PacienteRepository.create({
                'dni': data['dni'],
                'nombres': data['nombres'],
                'apellidos': data['apellidos'],
                'fecha_nacimiento': data['fecha_nacimiento'],
                'telefono': data.get('telefono', '')
            })

        orden = OrdenInternamientoRepository.create({
            'paciente': paciente,
            'especialidad_solicitada': data['especialidad'],
            'medico_solicitante': data['medico_solicitante']
        })
        return orden

    @staticmethod
    def verificar_disponibilidad(orden_id):
        orden = OrdenInternamientoRepository.get_by_id(orden_id)
        if not orden:
            raise ValidationError("Orden no encontrada")

        cama = CamaRepository.find_available_by_specialty(orden.especialidad_solicitada)
        if not cama:
            OrdenInternamientoRepository.update_estado(orden, 'EN_ESPERA')
            return {'disponible': False, 'mensaje': 'No hay camas disponibles', 'orden': orden.id}
        else:
            OrdenInternamientoRepository.update_estado(orden, 'VALIDADA')
            return {'disponible': True, 'cama': cama.numero, 'orden': orden.id}

    @staticmethod
    def validar_cobertura_sis(orden_id, codigo_sis):
        # Simulación: si el código empieza con 'SIS' es válido
        if codigo_sis and codigo_sis.startswith('SIS'):
            return {'valida': True}
        else:
            orden = OrdenInternamientoRepository.get_by_id(orden_id)
            OrdenInternamientoRepository.update_estado(orden, 'RECHAZADA')
            return {'valida': False, 'mensaje': 'Cobertura SIS inválida o inactiva'}

    @staticmethod
    def iniciar_hospitalizacion(orden_id, signos_vitales):
        orden = OrdenInternamientoRepository.get_by_id(orden_id)
        if not orden or orden.estado != 'VALIDADA':
            raise ValidationError("La orden no está validada")

        cama = CamaRepository.find_available_by_specialty(orden.especialidad_solicitada)
        if not cama:
            raise ValidationError("No hay cama disponible")

        CamaRepository.update_disponibilidad(cama, False)

        hospitalizacion = HospitalizacionRepository.create({
            'orden': orden,
            'cama': cama,
            'signos_vitales': signos_vitales
        })

        HistoriaClinicaRepository.create({
            'paciente': orden.paciente,
            'hospitalizacion': hospitalizacion
        })

        orden.estado = 'FINALIZADA'
        orden.save()

        return {
            'mensaje': 'Hospitalización exitosa',
            'hospitalizacion_id': hospitalizacion.id,
            'cama': cama.numero,
            'paciente': f"{orden.paciente.nombres} {orden.paciente.apellidos}"
        }
