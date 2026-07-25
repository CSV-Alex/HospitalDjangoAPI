from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.campana_vacunacion.interfaces.services import (
    VacunaService, LoteService, CampanaService,
    RegistroVacunacionService, PoblacionService,
)


# Controladores para Vacuna
@api_view(['POST'])
def crear_vacuna(request):
    """Crear una nueva vacuna"""
    try:
        service = VacunaService(None)  # Aquí se inyectaría el repositorio
        nombre = request.data.get('nombre')
        tipo = request.data.get('tipo')
        fabricante = request.data.get('fabricante')
        descripcion = request.data.get('descripcion')
        temp_min = request.data.get('tempconserv_min', 0.0)
        temp_max = request.data.get('tempconserv_max', 0.0)

        vacuna = service.crear_vacuna(nombre, tipo, fabricante, descripcion, temp_min, temp_max)
        return Response({'id': vacuna.id, 'nombre': vacuna.nombre}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_vacuna(request, vacuna_id):
    """Obtener una vacuna por ID"""
    try:
        service = VacunaService(None)
        vacuna = service.obtener_vacuna(vacuna_id)
        if vacuna:
            return Response({'id': vacuna.id, 'nombre': vacuna.nombre, 'tipo': vacuna.tipo})
        return Response({'error': 'Vacuna no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_vacunas(request):
    """Listar todas las vacunas"""
    try:
        service = VacunaService(None)
        vacunas = service.listar_vacunas()
        data = [{'id': v.id, 'nombre': v.nombre, 'tipo': v.tipo, 'fabricante': v.fabricante} 
                for v in vacunas]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def actualizar_vacuna(request, vacuna_id):
    """Actualizar una vacuna"""
    try:
        service = VacunaService(None)
        vacuna = service.actualizar_vacuna(vacuna_id, **request.data)
        return Response({'id': vacuna.id, 'mensaje': 'Vacuna actualizada correctamente'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_vacuna(request, vacuna_id):
    """Eliminar una vacuna"""
    try:
        service = VacunaService(None)
        service.eliminar_vacuna(vacuna_id)
        return Response({'mensaje': 'Vacuna eliminada correctamente'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Controladores para Lote
@api_view(['POST'])
def crear_lote(request):
    """Crear un nuevo lote"""
    try:
        service = LoteService(None)
        vacuna_id = request.data.get('vacuna_id')
        num_lote = request.data.get('num_lote')
        fecha_fab = request.data.get('fecha_fab')
        fecha_venc = request.data.get('fecha_venc')
        cantidad = request.data.get('cantidad', 0)

        lote = service.crear_lote(vacuna_id, num_lote, fecha_fab, fecha_venc, cantidad)
        return Response({'id': lote.id, 'num_lote': lote.num_lote}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_lotes(request):
    """Listar todos los lotes"""
    try:
        service = LoteService(None)
        lotes = service.listar_lotes()
        data = [{'id': l.id, 'num_lote': l.num_lote, 'vacuna_id': l.vacuna_id, 
                'cantidad': l.cantidad, 'cantidad_usada': l.cantidad_usada, 'estado': l.estado}
                for l in lotes]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_lotes_por_vacuna(request, vacuna_id):
    """Listar lotes de una vacuna específica"""
    try:
        service = LoteService(None)
        lotes = service.listar_lotes_por_vacuna(vacuna_id)
        data = [{'id': l.id, 'num_lote': l.num_lote, 'cantidad': l.cantidad} for l in lotes]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Controladores para Campana
@api_view(['POST'])
def crear_campana(request):
    """Crear una nueva campana"""
    try:
        service = CampanaService(None)
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        objetivo = request.data.get('objetivo')
        poblacion_objetivo = request.data.get('poblacion_objetivo')
        vacuna_id = request.data.get('vacuna_id')
        responsable = request.data.get('responsable')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        campana = service.crear_campana(nombre, descripcion, objetivo, poblacion_objetivo,
                                       vacuna_id, responsable, fecha_inicio, fecha_fin)
        return Response({'id': campana.id, 'nombre': campana.nombre}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_campanas(request):
    """Listar todas las campanas"""
    try:
        service = CampanaService(None)
        campanas = service.listar_campanas()
        data = [{'id': c.id, 'nombre': c.nombre, 'objetivo': c.objetivo, 
                'estado': c.estado, 'responsable': c.responsable} for c in campanas]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_campana(request, campana_id):
    """Obtener una campana por ID"""
    try:
        service = CampanaService(None)
        campana = service.obtener_campana(campana_id)
        if campana:
            return Response({
                'id': campana.id,
                'nombre': campana.nombre,
                'descripcion': campana.descripcion,
                'objetivo': campana.objetivo,
                'estado': campana.estado
            })
        return Response({'error': 'Campana no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Controladores para RegistroVacunacion
@api_view(['POST'])
def registrar_vacunacion(request):
    """Registrar una nueva vacunación"""
    try:
        service = RegistroVacunacionService(None)
        campana_id = request.data.get('campana_id')
        nombres = request.data.get('nombres')
        apellidos = request.data.get('apellidos')
        cedula = request.data.get('cedula')
        edad = request.data.get('edad', 0)
        sexo = request.data.get('sexo')
        lote_id = request.data.get('lote_id')
        sitio_vacunacion = request.data.get('sitio_vacunacion')
        personal_vacunador = request.data.get('personal_vacunador')
        observaciones = request.data.get('observaciones', '')

        registro = service.registrar_vacunacion(
            campana_id, nombres, apellidos, cedula, edad, sexo, lote_id,
            sitio_vacunacion, personal_vacunador, observaciones
        )
        return Response({'id': registro.id, 'cedula': registro.cedula}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_registros(request):
    """Listar todos los registros"""
    try:
        service = RegistroVacunacionService(None)
        registros = service.listar_registros()
        data = [{'id': r.id, 'cedula': r.cedula, 'nombres': r.nombres, 
                'apellidos': r.apellidos, 'fecha_vacunacion': r.fecha_vacunacion}
                for r in registros]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_registros_por_campana(request, campana_id):
    """Listar registros de una campana específica"""
    try:
        service = RegistroVacunacionService(None)
        registros = service.listar_registros_por_campana(campana_id)
        data = [{'id': r.id, 'cedula': r.cedula, 'nombres': r.nombres, 'apellidos': r.apellidos}
                for r in registros]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Controladores para Poblacion
@api_view(['POST'])
def crear_poblacion(request):
    """Crear un grupo de población objetivo"""
    try:
        service = PoblacionService(None)
        campana_id = request.data.get('campana_id')
        grupo_edad_min = request.data.get('grupo_edad_min', 0)
        grupo_edad_max = request.data.get('grupo_edad_max', 150)
        descripcion = request.data.get('descripcion')
        cantidad_estimada = request.data.get('cantidad_estimada', 0)

        poblacion = service.crear_poblacion(campana_id, grupo_edad_min, grupo_edad_max, 
                                           descripcion, cantidad_estimada)
        return Response({'id': poblacion.id, 'descripcion': poblacion.descripcion}, 
                       status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_poblaciones_por_campana(request, campana_id):
    """Listar grupos de población de una campana específica"""
    try:
        service = PoblacionService(None)
        poblaciones = service.listar_poblaciones_por_campana(campana_id)
        data = [{'id': p.id, 'descripcion': p.descripcion, 'grupo_edad_min': p.grupo_edad_min,
                'grupo_edad_max': p.grupo_edad_max, 'cantidad_estimada': p.cantidad_estimada}
                for p in poblaciones]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
