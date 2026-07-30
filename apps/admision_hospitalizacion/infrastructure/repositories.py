import logging
from typing import Optional
from ..domain.entities import HospitalizacionRequest
from ..domain.exceptions import PacienteNoEncontradoException, CamaNoDisponibleException
from ..models import Paciente, Cama, OrdenInternamiento, Hospitalizacion

logger = logging.getLogger(__name__)

class HospitalizacionRepositoryDjango:
    """Adaptador de repositorio que persiste la entidad de dominio usando modelos Django."""
    
    def save(self, request: HospitalizacionRequest) -> None:
        dni = request.dni_paciente.valor
        codigo_cama = request.codigo_cama.valor
        especialidad = request.especialidad.valor
        
        # 1. Buscar paciente
        try:
            paciente_db = Paciente.objects.get(dni=dni)
        except Paciente.DoesNotExist:
            logger.error("Paciente con DNI %s no encontrado en DB.", dni)
            raise PacienteNoEncontradoException(dni)
            
        # 2. Buscar cama disponible
        try:
            cama_db = Cama.objects.get(numero=codigo_cama, disponible=True)
        except Cama.DoesNotExist:
            logger.error("Cama %s no disponible o no encontrada.", codigo_cama)
            raise CamaNoDisponibleException(codigo_cama)
            
        # 3. Crear Orden de Internamiento (asumiendo que Bonita nos manda para crear una nueva)
        orden = OrdenInternamiento.objects.create(
            paciente=paciente_db,
            especialidad_solicitada=especialidad,
            medico_solicitante="Sistema Bonita BPM",  # O un dato del payload
            estado='VALIDADA'
        )
        
        # 4. Crear Hospitalización y ocupar cama
        Hospitalizacion.objects.create(
            orden=orden,
            cama=cama_db,
            estado='ACTIVA'
        )
        
        cama_db.disponible = False
        cama_db.save()
        logger.info("Hospitalización registrada correctamente en la BD.")
