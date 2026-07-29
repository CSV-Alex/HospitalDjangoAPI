from rest_framework import serializers
from .models import Cita, HistoriaClinica, Paciente, PeticionPrueba, Triaje


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class PacienteNecesitaExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['necesita_examen']


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'


class TriajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triaje
        fields = '__all__'


class HistoriaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'


class HistoriaClinicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinica
        fields = ['diagnostico', 'tratamiento', 'receta_medica']


class PeticionPruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeticionPrueba
        fields = '__all__'