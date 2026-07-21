from django.urls import path
from apps.pruebas_laboratorio.interfaces.views import (
    PacienteView, SolicitudPruebaView, ResultadoPruebaView,
)

app_name = 'pruebas_laboratorio'

urlpatterns = [
    path('pacientes/', PacienteView.as_view(), name='paciente-list'),
    path('pacientes/<int:pk>/', PacienteView.as_view(), name='paciente-detail'),
    path('solicitudes/', SolicitudPruebaView.as_view(), name='solicitud-prueba-list'),
    path('solicitudes/<int:pk>/', SolicitudPruebaView.as_view(), name='solicitud-prueba-detail'),
    path('resultados/', ResultadoPruebaView.as_view(), name='resultado-prueba-list'),
    path('resultados/<int:pk>/', ResultadoPruebaView.as_view(), name='resultado-prueba-detail')
]
