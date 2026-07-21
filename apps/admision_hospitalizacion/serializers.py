from rest_framework import serializers
from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class CamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cama
        fields = '__all__'

class OrdenInternamientoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(), source='paciente', write_only=True
    )

    class Meta:
        model = OrdenInternamiento
        fields = '__all__'

class HospitalizacionSerializer(serializers.ModelSerializer):
    orden = OrdenInternamientoSerializer(read_only=True)
    cama = CamaSerializer(read_only=True)

    class Meta:
        model = Hospitalizacion
        fields = '__all__'

class RecepcionOrdenSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    fecha_nacimiento = serializers.DateField()
    telefono = serializers.CharField(max_length=15, required=False, allow_blank=True)
    especialidad = serializers.CharField(max_length=50)
    medico_solicitante = serializers.CharField(max_length=100)

class ValidarCoberturaSerializer(serializers.Serializer):
    codigo_sis = serializers.CharField(max_length=20)

class IniciarHospitalizacionSerializer(serializers.Serializer):
    signos_vitales = serializers.JSONField()
