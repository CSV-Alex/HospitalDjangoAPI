"""
URLs para endpoints integrados con Bonita
"""
from django.urls import path
from apps.campana_vacunacion.interfaces.bonita_views import (
    # Campanas con Bonita
    crear_campana_con_bonita,
    obtener_campana_con_bonita,
    # Registros con Bonita
    registrar_vacunacion_con_bonita,
    listar_registros_por_campana_con_bonita,
    # Tareas de Bonita
    obtener_tareas_campana,
    completar_tarea_campana,
    # Flujo completo
    inicializar_flujo_campana,
    obtener_estado_flujo,
    # Utilidades
    listar_procesos_disponibles,
    listar_instancias_proceso,
)

urlpatterns = [
    # =====================================================================
    # CAMPAnAS CON BONITA
    # =====================================================================
    path('bonita/campanas/crear/', 
         crear_campana_con_bonita, 
         name='crear_campana_con_bonita'),
    
    path('bonita/campanas/<int:campana_id>/<str:bonita_instance_id>/', 
         obtener_campana_con_bonita, 
         name='obtener_campana_con_bonita'),
    
    # =====================================================================
    # REGISTROS CON BONITA
    # =====================================================================
    path('bonita/registros/crear/', 
         registrar_vacunacion_con_bonita, 
         name='registrar_vacunacion_con_bonita'),
    
    path('bonita/registros/campana/<int:campana_id>/<str:bonita_instance_id>/', 
         listar_registros_por_campana_con_bonita, 
         name='listar_registros_por_campana_con_bonita'),
    
    # =====================================================================
    # TAREAS DE BONITA
    # =====================================================================
    path('bonita/tareas/<str:bonita_instance_id>/', 
         obtener_tareas_campana, 
         name='obtener_tareas_campana'),
    
    path('bonita/tareas/<str:bonita_instance_id>/<str:task_id>/completar/', 
         completar_tarea_campana, 
         name='completar_tarea_campana'),
    
    # =====================================================================
    # FLUJO COMPLETO
    # =====================================================================
    path('bonita/flujo/inicializar/', 
         inicializar_flujo_campana, 
         name='inicializar_flujo_campana'),
    
    path('bonita/flujo/<str:bonita_instance_id>/estado/', 
         obtener_estado_flujo, 
         name='obtener_estado_flujo'),
    
    # =====================================================================
    # UTILIDADES
    # =====================================================================
    path('bonita/procesos/', 
         listar_procesos_disponibles, 
         name='listar_procesos_disponibles'),
    
    path('bonita/instancias/', 
         listar_instancias_proceso, 
         name='listar_instancias_proceso'),
]
