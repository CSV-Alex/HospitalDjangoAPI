import logging
from typing import Optional, List

from ..domain.repositories import PacienteRepository
from ..domain.entities import Paciente
from ..domain.value_objects import NumeroHistoriaClinica
from ..domain.exceptions import RepositoryException
from ..models import Paciente as PacienteORM

logger = logging.getLogger(__name__)

class PacienteRepositoryDjango(PacienteRepository):
    
    def save(self, paciente: Paciente) -> None:
        try:
            paciente_orm, creado = PacienteORM.objects.get_or_create(
                numero_historia_clinica=paciente.numero_historia_clinica.valor,
                defaults={
                    'dni': '',
                    'nombre_completo': paciente.nombre_completo.valor,
                    'fecha_nacimiento': paciente.fecha_nacimiento.valor,
                    'necesita_examen': paciente.necesita_examen.valor,
                }
            )
            
            if not creado:
                paciente_orm.nombre_completo = paciente.nombre_completo.valor
                paciente_orm.fecha_nacimiento = paciente.fecha_nacimiento.valor
                paciente_orm.necesita_examen = paciente.necesita_examen.valor
                paciente_orm.save()
            
            logger.info(
                f"Paciente guardado: {paciente.numero_historia_clinica.valor} "
                f"({paciente.nombre_completo.valor})"
            )
        
        except Exception as e:
            logger.error(f"Error al guardar Paciente: {str(e)}", exc_info=True)
            raise RepositoryException(
                f"Error al guardar Paciente en BD: {str(e)}"
            )
    
    def find_by_id(self, paciente_id: str) -> Optional[Paciente]:
        try:
            paciente_orm = PacienteORM.objects.get(id=paciente_id)
            return self._orm_to_entity(paciente_orm)
        
        except PacienteORM.DoesNotExist:
            logger.warning(f"Paciente no encontrado por ID: {paciente_id}")
            return None
        
        except Exception as e:
            logger.error(f"Error al buscar Paciente por ID: {str(e)}", exc_info=True)
            raise RepositoryException(f"Error al buscar Paciente: {str(e)}")
    
    def find_by_numero_historia_clinica(
        self, numero_historia: NumeroHistoriaClinica
    ) -> Optional[Paciente]:
        try:
            paciente_orm = PacienteORM.objects.get(
                numero_historia_clinica=numero_historia.valor
            )
            return self._orm_to_entity(paciente_orm)
        
        except PacienteORM.DoesNotExist:
            logger.info(f"Paciente no encontrado: {numero_historia.valor}")
            return None
        
        except Exception as e:
            logger.error(
                f"Error al buscar Paciente por número: {str(e)}", 
                exc_info=True
            )
            raise RepositoryException(f"Error al buscar Paciente: {str(e)}")
    
    def find_all(self) -> List[Paciente]:
        try:
            pacientes_orm = PacienteORM.objects.all()
            return [self._orm_to_entity(p) for p in pacientes_orm]
        
        except Exception as e:
            logger.error(f"Error al obtener todos los Pacientes: {str(e)}", exc_info=True)
            raise RepositoryException(f"Error al obtener Pacientes: {str(e)}")
    
    def update(self, paciente: Paciente) -> None:
        try:
            paciente_orm = PacienteORM.objects.get(
                numero_historia_clinica=paciente.numero_historia_clinica.valor
            )
            
            paciente_orm.nombre_completo = paciente.nombre_completo.valor
            paciente_orm.fecha_nacimiento = paciente.fecha_nacimiento.valor
            paciente_orm.necesita_examen = paciente.necesita_examen.valor
            paciente_orm.save()
            
            logger.info(f"Paciente actualizado: {paciente.numero_historia_clinica.valor}")
        
        except PacienteORM.DoesNotExist:
            logger.error(f"Paciente no encontrado para actualizar")
            raise RepositoryException("Paciente no encontrado")
        
        except Exception as e:
            logger.error(f"Error al actualizar Paciente: {str(e)}", exc_info=True)
            raise RepositoryException(f"Error al actualizar Paciente: {str(e)}")
    
    def delete(self, paciente_id: str) -> None:
        try:
            PacienteORM.objects.filter(numero_historia_clinica=paciente_id).delete()
            logger.info(f"Paciente eliminado: {paciente_id}")
        
        except Exception as e:
            logger.error(f"Error al eliminar Paciente: {str(e)}", exc_info=True)
            raise RepositoryException(f"Error al eliminar Paciente: {str(e)}")
    
    @staticmethod
    def _orm_to_entity(paciente_orm: PacienteORM) -> Paciente:
        from ..domain.value_objects import (
            NumeroHistoriaClinica,
            NombreCompleto,
            FechaNacimiento,
            NecesitaExamen,
        )
        
        return Paciente(
            numero_historia_clinica=NumeroHistoriaClinica(
                str(paciente_orm.numero_historia_clinica)
            ),
            nombre_completo=NombreCompleto(paciente_orm.nombre_completo),
            fecha_nacimiento=FechaNacimiento(paciente_orm.fecha_nacimiento),
            necesita_examen=NecesitaExamen(paciente_orm.necesita_examen),
            id=str(paciente_orm.id),
        )