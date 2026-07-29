from django.contrib import admin
from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'fecha_nacimiento')
    search_fields = ('dni', 'nombres', 'apellidos')

@admin.register(Cama)
class CamaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'especialidad', 'disponible')
    list_filter = ('disponible', 'especialidad')

@admin.register(OrdenInternamiento)
class OrdenInternamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'especialidad_solicitada', 'estado', 'fecha_emision')
    list_filter = ('estado', 'especialidad_solicitada')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'medico_solicitante')

@admin.register(Hospitalizacion)
class HospitalizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'cama', 'fecha_ingreso', 'estado')
    list_filter = ('estado',)

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'hospitalizacion', 'fecha_apertura')
    search_fields = ('paciente__nombres', 'paciente__apellidos')
