from django.urls import path, include
from apps.campana_vacunacion.interfaces.views import (
    # Vacuna
    crear_vacuna,
    obtener_vacuna,
    listar_vacunas,
    actualizar_vacuna,
    eliminar_vacuna,
    # Lote
    crear_lote,
    listar_lotes,
    listar_lotes_por_vacuna,
    # Campana
    crear_campana,
    obtener_campana,
    listar_campanas,
    # RegistroVacunacion
    registrar_vacunacion,
    listar_registros,
    listar_registros_por_campana,
    # Poblacion
    crear_poblacion,
    listar_poblaciones_por_campana,
)

from apps.campana_vacunacion.interfaces.swagger_views import (
    swagger_json_view,
    swagger_ui_view,
)

urlpatterns = [
    # ========================================================================
    # SWAGGER / OPENAPI DOCUMENTATION
    # ========================================================================
    path('swagger/', swagger_ui_view, name='swagger_ui'),
    path('swagger.json', swagger_json_view, name='swagger_json'),

    # ========================================================================
    # ENDPOINTS MOCK (sin Bonita)
    # ========================================================================
    
    # URLs para Vacuna
    path('vacunas/', listar_vacunas, name='listar_vacunas'),
    path('vacunas/crear/', crear_vacuna, name='crear_vacuna'),
    path('vacunas/<int:vacuna_id>/', obtener_vacuna, name='obtener_vacuna'),
    path('vacunas/<int:vacuna_id>/actualizar/', actualizar_vacuna, name='actualizar_vacuna'),
    path('vacunas/<int:vacuna_id>/eliminar/', eliminar_vacuna, name='eliminar_vacuna'),
    
    # URLs para Lote
    path('lotes/', listar_lotes, name='listar_lotes'),
    path('lotes/crear/', crear_lote, name='crear_lote'),
    path('lotes/vacuna/<int:vacuna_id>/', listar_lotes_por_vacuna, name='listar_lotes_por_vacuna'),
    
    # URLs para Campana (mock)
    path('campanas/', listar_campanas, name='listar_campanas'),
    path('campanas/crear/', crear_campana, name='crear_campana'),
    path('campanas/<int:campana_id>/', obtener_campana, name='obtener_campana'),
    
    # URLs para RegistroVacunacion (mock)
    path('registros/', listar_registros, name='listar_registros'),
    path('registros/crear/', registrar_vacunacion, name='registrar_vacunacion'),
    path('registros/campana/<int:campana_id>/', listar_registros_por_campana, name='listar_registros_por_campana'),
    
    # URLs para Poblacion
    path('poblaciones/crear/', crear_poblacion, name='crear_poblacion'),
    path('poblaciones/campana/<int:campana_id>/', listar_poblaciones_por_campana, name='listar_poblaciones_por_campana'),
    
    # ========================================================================
    # ENDPOINTS CON BONITA
    # ========================================================================
    path('', include('apps.campana_vacunacion.interfaces.bonita_urls')),
]

