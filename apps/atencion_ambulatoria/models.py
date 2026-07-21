from django.db import models


class Paciente(models.Model):
    numero_historia_clinica = models.BigIntegerField(unique=True)
    dni = models.CharField(max_length=8, unique=True)
    nombre_completo = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    necesita_examen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"


class Cita(models.Model):
    ESTADO_PROGRAMADA = 'PROGRAMADA'
    ESTADO_EN_TRIAGE = 'EN_TRIAGE'
    ESTADO_EN_CONSULTA = 'EN_CONSULTA'
    ESTADO_FINALIZADA = 'FINALIZADA'

    ESTADO_CHOICES = [
        (ESTADO_PROGRAMADA, 'Programada'),
        (ESTADO_EN_TRIAGE, 'En Triaje'),
        (ESTADO_EN_CONSULTA, 'En Consulta'),
        (ESTADO_FINALIZADA, 'Finalizada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PROGRAMADA)

    def __str__(self):
        return f"Cita de {self.paciente.nombre_completo} - {self.fecha_hora}"


class Triaje(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='triajes')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    presion_sistolica = models.IntegerField()
    presion_diastolica = models.IntegerField()
    temperatura = models.FloatField()

    def __str__(self):
        return f"Triaje de {self.paciente.nombre_completo} - {self.fecha_hora}"


class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historia_clinica')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    receta_medica = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Historia clínica de {self.paciente.nombre_completo}"


class PeticionPrueba(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='peticiones_prueba')
    tipo_examen = models.CharField(max_length=255)
    tiene_sis = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Petición de prueba: {self.tipo_examen} - {self.paciente.nombre_completo}"