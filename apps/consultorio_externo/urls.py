from django.urls import path
from .views import (
    CitaListCreateAPIView,
    HistoriaClinicaDetailAPIView,
    HistoriaClinicaListCreateAPIView,
    PacienteCreateAPIView,
    PacientePatchAPIView,
    PeticionPruebaCreateAPIView,
    TriajeCreateAPIView,
)

urlpatterns = [
    path('pacientes/', PacienteCreateAPIView.as_view(), name='paciente-create'),
    path('pacientes/<int:pk>/', PacientePatchAPIView.as_view(), name='paciente-patch'),

    path('citas/', CitaListCreateAPIView.as_view(), name='cita-list-create'),

    path('triaje/', TriajeCreateAPIView.as_view(), name='triaje-create'),

    path('historias-clinicas/', HistoriaClinicaListCreateAPIView.as_view(), name='historia-create'),
    path('historias-clinicas/<int:pk>/', HistoriaClinicaDetailAPIView.as_view(), name='historia-patch'),

    path('peticiones-prueba/', PeticionPruebaCreateAPIView.as_view(), name='peticion-create'),
]