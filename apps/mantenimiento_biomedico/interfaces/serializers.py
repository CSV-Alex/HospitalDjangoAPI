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


class ReporteSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    equipo_id = serializers.IntegerField(required=False, allow_null=True)
    descripcion = serializers.CharField()
    reportado_por = serializers.CharField(max_length=200)
    fecha = serializers.DateTimeField(required=False)
    estado = EnumField()


class EvalSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    reporte_id = serializers.IntegerField(required=False, allow_null=True)
    tecnico = serializers.CharField(max_length=200)
    diagnostico = serializers.CharField()
    reemplazo = serializers.BooleanField()
    fecha = serializers.DateTimeField(required=False)


class SolicitudSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    eval_id = serializers.IntegerField(required=False, allow_null=True)
    equipo_id = serializers.IntegerField(required=False, allow_null=True)
    motivo = serializers.CharField()
    fecha = serializers.DateTimeField(required=False)
    estado = EnumField()


class EstimacionSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    solicitud_id = serializers.IntegerField(required=False, allow_null=True)
    precio = serializers.DecimalField(max_digits=12, decimal_places=2)
    proveedor = serializers.CharField(max_length=200)
    detalle = serializers.CharField()
    fecha = serializers.DateTimeField(required=False)


class IntervSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    equipo_id = serializers.IntegerField(required=False, allow_null=True)
    solicitud_id = serializers.IntegerField(required=False, allow_null=True)
    tipo = EnumField()
    descripcion = serializers.CharField()
    tecnico = serializers.CharField(max_length=200)
    fecha_ini = serializers.DateTimeField(required=False)
    fecha_fin = serializers.DateTimeField(required=False, allow_null=True)
    resultado = serializers.CharField(required=False, allow_null=True)
    obs = serializers.CharField(required=False, allow_null=True)
