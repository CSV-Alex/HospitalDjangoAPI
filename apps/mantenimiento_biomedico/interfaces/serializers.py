from rest_framework import serializers


class EnumField(serializers.Field):

    def to_representation(self, value):
        if hasattr(value, 'value'):
            return value.value
        return str(value)

    def to_internal_value(self, data):
        return data


class EquipoSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    codigo = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=200)
    tipo = EnumField()
    fabricante = serializers.CharField(max_length=200)
    modelo = serializers.CharField(max_length=100)
    num_serie = serializers.CharField(max_length=100)
    ubicacion = serializers.CharField(max_length=200)
    fecha_adq = serializers.DateField(required=False, allow_null=True)
    fecha_ult_calib = serializers.DateField(required=False, allow_null=True)
    estado = EnumField()
