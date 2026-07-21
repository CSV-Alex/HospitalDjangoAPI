from rest_framework import serializers



class PacienteSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=200)
    apellido = serializers.CharField(max_length=200)
    fecha_nac = serializers.DateField()
    genero = serializers.CharField(max_length=10)
    dni = serializers.CharField(max_length=20)
    direccion = serializers.CharField(max_length=300)
    telefono = serializers.CharField(max_length=20, required=False, allow_null=True)


class SolicitudPruebaSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    paciente_id = serializers.IntegerField()
    tipo_prueba = serializers.CharField(max_length=200)
    fecha_solicitud = serializers.DateTimeField(required=False)
    estado = serializers.CharField(max_length=50)

class ResultadoPruebaSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    solicitud_id = serializers.IntegerField()
    resultado = serializers.CharField()
    fecha_resultado = serializers.DateTimeField(required=False)