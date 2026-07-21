from django.db import models

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nac = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'mb_paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id})"

class SolicitudPrueba(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='solicitudes_prueba')
    paciente_id = models.IntegerField()
    tipo_prueba = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, default='Pendiente')

    class Meta:
        db_table = 'mb_solicitud_prueba'
        verbose_name = 'Solicitud de Prueba'
        verbose_name_plural = 'Solicitudes de Prueba'

    def __str__(self):
        return f"SolicitudPrueba #{self.id} - Paciente {self.paciente.nombre} {self.paciente.apellido}"


class ResultadoPrueba(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudPrueba, on_delete=models.CASCADE, related_name='resultados_prueba')
    solicitud_id = models.IntegerField()
    resultado = models.TextField()
    fecha_resultado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mb_resultado_prueba'
        verbose_name = 'Resultado de Prueba'
        verbose_name_plural = 'Resultados de Prueba'

    def __str__(self):
        return f"ResultadoPrueba #{self.id} - Solicitud {self.solicitud.id}"
