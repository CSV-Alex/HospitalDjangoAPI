from django.contrib import admin
from .models import Paciente, Cita, Triaje, HistoriaClinica, PeticionPrueba

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        'numero_historia_clinica',
        'dni',
        'nombre_completo',
        'fecha_nacimiento',
        'necesita_examen',
    )
    list_filter = ('necesita_examen', 'fecha_nacimiento')
    search_fields = ('numero_historia_clinica', 'dni', 'nombre_completo')
    readonly_fields = ('id',)
    ordering = ('-id',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('numero_historia_clinica', 'dni', 'nombre_completo', 'fecha_nacimiento')
        }),
        ('Exámenes', {
            'fields': ('necesita_examen',)
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('paciente__nombre_completo',)
    readonly_fields = ('id',)
    
    fieldsets = (
        ('Información de Cita', {
            'fields': ('paciente', 'fecha_hora', 'estado')
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Triaje)
class TriajeAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_hora', 'presion_sistolica', 'presion_diastolica', 'temperatura')
    list_filter = ('fecha_hora',)
    search_fields = ('paciente__nombre_completo',)
    readonly_fields = ('id', 'fecha_hora')
    
    fieldsets = (
        ('Información del Triaje', {
            'fields': ('paciente', 'presion_sistolica', 'presion_diastolica', 'temperatura')
        }),
        ('Fecha', {
            'fields': ('fecha_hora',)
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('paciente__nombre_completo',)
    readonly_fields = ('id', 'fecha_creacion')
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'fecha_creacion')
        }),
        ('Diagnóstico y Tratamiento', {
            'fields': ('diagnostico', 'tratamiento', 'receta_medica')
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PeticionPrueba)
class PeticionPruebaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_examen', 'tiene_sis', 'fecha_solicitud')
    list_filter = ('tiene_sis', 'fecha_solicitud')
    search_fields = ('paciente__nombre_completo', 'tipo_examen')
    readonly_fields = ('id', 'fecha_solicitud')
    
    fieldsets = (
        ('Información de Prueba', {
            'fields': ('paciente', 'tipo_examen', 'tiene_sis')
        }),
        ('Fecha', {
            'fields': ('fecha_solicitud',)
        }),
        ('Metadata', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )