from rest_framework import serializers
from datetime import date

class PacienteListSerializer(serializers.Serializer):
    
    numero_historia_clinica = serializers.CharField(
        max_length=50,
        help_text="Número único de historia clínica"
    )
    nombre_completo = serializers.CharField(
        max_length=255,
        help_text="Nombre completo del paciente"
    )
    fecha_nacimiento = serializers.DateField(
        help_text="Fecha de nacimiento (YYYY-MM-DD)"
    )
    necesita_examen = serializers.BooleanField(
        help_text="El paciente necesita examen de laboratorio?"
    )
    edad = serializers.IntegerField(
        read_only=True,
        help_text="Edad calculada del paciente"
    )


class PacienteCreateSerializer(serializers.Serializer):
    """crear/registrar Pacientes desde Bonita."""
    
    numeroHistoriaClinica = serializers.CharField(
        max_length=50,
        required=True,
        help_text="Número único de historia clínica enviado por Bonita"
    )
    nombreCompleto = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Nombre completo del paciente"
    )
    fechaNacimiento = serializers.CharField(
        required=True,
        help_text="Fecha de nacimiento (YYYY-MM-DD)"
    )
    necesitaExamen = serializers.BooleanField(
        required=True,
        help_text="¿Necesita examen de laboratorio?"
    )


class ConsultaResponseSerializer(serializers.Serializer):
    """la respuesta de registro de consulta"""
    
    status = serializers.CharField(
        help_text="Estado de la operación: 'success' o 'error'"
    )
    message = serializers.CharField(
        help_text="Mensaje descriptivo de la operación"
    )
    necesita_examen = serializers.BooleanField(
        required=False,
        help_text="El paciente necesita examen?"
    )
    data = serializers.DictField(
        required=False,
        help_text="Datos del paciente registrado"
    )