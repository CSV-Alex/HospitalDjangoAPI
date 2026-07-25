from typing import List, Optional
from apps.campana_vacunacion.domain.entities import (
    Vacuna, Lote, Campana, RegistroVacunacion,
    Poblacion,
)
from apps.campana_vacunacion.domain.repository_interfaces import (
    IVacunaRepo, ILoteRepo, ICampanaRepo, IRegistroVacunacionRepo,
    IPoblacionRepo,
)


class VacunaService:
    def __init__(self, repo: IVacunaRepo):
        self.repo = repo

    def crear_vacuna(self, nombre: str, tipo: str, fabricante: str,
                     descripcion: str, temp_min: float, temp_max: float) -> Vacuna:
        """Crear una nueva vacuna"""
        vacuna = Vacuna(
            nombre=nombre,
            tipo=tipo,
            fabricante=fabricante,
            descripcion=descripcion,
            tempconserv_min=temp_min,
            tempconserv_max=temp_max
        )
        return self.repo.save(vacuna)

    def obtener_vacuna(self, vacuna_id: int) -> Optional[Vacuna]:
        """Obtener una vacuna por ID"""
        return self.repo.find_by_id(vacuna_id)

    def listar_vacunas(self) -> List[Vacuna]:
        """Listar todas las vacunas"""
        return self.repo.find_all()

    def actualizar_vacuna(self, vacuna_id: int, **kwargs) -> Vacuna:
        """Actualizar una vacuna"""
        vacuna = self.repo.find_by_id(vacuna_id)
        if not vacuna:
            raise ValueError(f"Vacuna con ID {vacuna_id} no encontrada")
        
        for key, value in kwargs.items():
            if hasattr(vacuna, key):
                setattr(vacuna, key, value)
        
        return self.repo.save(vacuna)

    def eliminar_vacuna(self, vacuna_id: int) -> None:
        """Eliminar una vacuna"""
        self.repo.delete(vacuna_id)


class LoteService:
    def __init__(self, repo: ILoteRepo):
        self.repo = repo

    def crear_lote(self, vacuna_id: int, num_lote: str,
                   fecha_fab, fecha_venc, cantidad: int) -> Lote:
        """Crear un nuevo lote de vacunas"""
        lote = Lote(
            vacuna_id=vacuna_id,
            num_lote=num_lote,
            fecha_fab=fecha_fab,
            fecha_venc=fecha_venc,
            cantidad=cantidad,
            cantidad_usada=0
        )
        return self.repo.save(lote)

    def obtener_lote(self, lote_id: int) -> Optional[Lote]:
        """Obtener un lote por ID"""
        return self.repo.find_by_id(lote_id)

    def listar_lotes(self) -> List[Lote]:
        """Listar todos los lotes"""
        return self.repo.find_all()

    def listar_lotes_por_vacuna(self, vacuna_id: int) -> List[Lote]:
        """Listar lotes de una vacuna específica"""
        return self.repo.find_by_vacuna(vacuna_id)

    def actualizar_lote(self, lote_id: int, **kwargs) -> Lote:
        """Actualizar un lote"""
        lote = self.repo.find_by_id(lote_id)
        if not lote:
            raise ValueError(f"Lote con ID {lote_id} no encontrado")
        
        for key, value in kwargs.items():
            if hasattr(lote, key):
                setattr(lote, key, value)
        
        return self.repo.save(lote)

    def eliminar_lote(self, lote_id: int) -> None:
        """Eliminar un lote"""
        self.repo.delete(lote_id)


class CampanaService:
    def __init__(self, repo: ICampanaRepo):
        self.repo = repo

    def crear_campana(self, nombre: str, descripcion: str, objetivo: str,
                      poblacion_objetivo: str, vacuna_id: int,
                      responsable: str, fecha_inicio, fecha_fin) -> Campana:
        """Crear una nueva campana de vacunación"""
        campana = Campana(
            nombre=nombre,
            descripcion=descripcion,
            objetivo=objetivo,
            poblacion_objetivo=poblacion_objetivo,
            vacuna_id=vacuna_id,
            responsable=responsable,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return self.repo.save(campana)

    def obtener_campana(self, campana_id: int) -> Optional[Campana]:
        """Obtener una campana por ID"""
        return self.repo.find_by_id(campana_id)

    def listar_campanas(self) -> List[Campana]:
        """Listar todas las campanas"""
        return self.repo.find_all()

    def actualizar_campana(self, campana_id: int, **kwargs) -> Campana:
        """Actualizar una campana"""
        campana = self.repo.find_by_id(campana_id)
        if not campana:
            raise ValueError(f"Campana con ID {campana_id} no encontrada")
        
        for key, value in kwargs.items():
            if hasattr(campana, key):
                setattr(campana, key, value)
        
        return self.repo.save(campana)

    def eliminar_campana(self, campana_id: int) -> None:
        """Eliminar una campana"""
        self.repo.delete(campana_id)


class RegistroVacunacionService:
    def __init__(self, repo: IRegistroVacunacionRepo):
        self.repo = repo

    def registrar_vacunacion(self, campana_id: int, nombres: str, apellidos: str,
                             cedula: str, edad: int, sexo: str, lote_id: int,
                             sitio_vacunacion: str, personal_vacunador: str,
                             observaciones: str = "") -> RegistroVacunacion:
        """Registrar una vacunación"""
        registro = RegistroVacunacion(
            campana_id=campana_id,
            nombres=nombres,
            apellidos=apellidos,
            cedula=cedula,
            edad=edad,
            sexo=sexo,
            lote_id=lote_id,
            sitio_vacunacion=sitio_vacunacion,
            personal_vacunador=personal_vacunador,
            observaciones=observaciones
        )
        return self.repo.save(registro)

    def obtener_registro(self, registro_id: int) -> Optional[RegistroVacunacion]:
        """Obtener un registro por ID"""
        return self.repo.find_by_id(registro_id)

    def listar_registros(self) -> List[RegistroVacunacion]:
        """Listar todos los registros"""
        return self.repo.find_all()

    def listar_registros_por_campana(self, campana_id: int) -> List[RegistroVacunacion]:
        """Listar registros de una campana específica"""
        return self.repo.find_by_campana(campana_id)

    def actualizar_registro(self, registro_id: int, **kwargs) -> RegistroVacunacion:
        """Actualizar un registro"""
        registro = self.repo.find_by_id(registro_id)
        if not registro:
            raise ValueError(f"Registro con ID {registro_id} no encontrado")
        
        for key, value in kwargs.items():
            if hasattr(registro, key):
                setattr(registro, key, value)
        
        return self.repo.save(registro)

    def eliminar_registro(self, registro_id: int) -> None:
        """Eliminar un registro"""
        self.repo.delete(registro_id)



class PoblacionService:
    def __init__(self, repo: IPoblacionRepo):
        self.repo = repo

    def crear_poblacion(self, campana_id: int, grupo_edad_min: int,
                       grupo_edad_max: int, descripcion: str,
                       cantidad_estimada: int) -> Poblacion:
        """Crear un grupo de población objetivo"""
        poblacion = Poblacion(
            campana_id=campana_id,
            grupo_edad_min=grupo_edad_min,
            grupo_edad_max=grupo_edad_max,
            descripcion=descripcion,
            cantidad_estimada=cantidad_estimada
        )
        return self.repo.save(poblacion)

    def obtener_poblacion(self, poblacion_id: int) -> Optional[Poblacion]:
        """Obtener un grupo de población por ID"""
        return self.repo.find_by_id(poblacion_id)

    def listar_poblaciones(self) -> List[Poblacion]:
        """Listar todos los grupos de población"""
        return self.repo.find_all()

    def listar_poblaciones_por_campana(self, campana_id: int) -> List[Poblacion]:
        """Listar grupos de población de una campana específica"""
        return self.repo.find_by_campana(campana_id)

    def actualizar_poblacion(self, poblacion_id: int, **kwargs) -> Poblacion:
        """Actualizar un grupo de población"""
        poblacion = self.repo.find_by_id(poblacion_id)
        if not poblacion:
            raise ValueError(f"Población con ID {poblacion_id} no encontrada")
        
        for key, value in kwargs.items():
            if hasattr(poblacion, key):
                setattr(poblacion, key, value)
        
        return self.repo.save(poblacion)

    def eliminar_poblacion(self, poblacion_id: int) -> None:
        """Eliminar un grupo de población"""
        self.repo.delete(poblacion_id)
