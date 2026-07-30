from django.urls import path
from .views import (
    RegistrarConsultaView,
    ListarPacientesView,
    ObtenerPacienteView,
)

app_name = 'consultorio_externo'

urlpatterns = [
    # Endpoint para registrar consultas
    path(
        'registrar/',
        RegistrarConsultaView.as_view(),
        name='registrar_consulta'
    ),
    
    # Endpoint para listar pacientes
    path(
        'pacientes/',
        ListarPacientesView.as_view(),
        name='listar_pacientes'
    ),
    
    # Endpoint para obtener un paciente específico
    path(
        'pacientes/<str:numero_historia_clinica>/',
        ObtenerPacienteView.as_view(),
        name='obtener_paciente'
    ),
]