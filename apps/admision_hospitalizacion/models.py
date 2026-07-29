from django.db import models
from django.core.validators import MinLengthValidator

class Paciente(models.Model):
    dni = models.CharField(max_length=8, unique=True, validators=[MinLengthValidator(8)])
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Cama(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    especialidad = models.CharField(max_length=50)  # Ej: Medicina Interna, Cirugía
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Cama {self.numero} - {self.especialidad}"

class OrdenInternamiento(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('VALIDADA', 'Validada'),
        ('RECHAZADA', 'Rechazada'),
        ('EN_ESPERA', 'En lista de espera'),
        ('FINALIZADA', 'Finalizada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidad_solicitada = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    medico_solicitante = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Orden {self.id} - {self.paciente}"

class Hospitalizacion(models.Model):
    ESTADOS_HOSP = [
        ('ACTIVA', 'Activa'),
        ('ALTA', 'Alta'),
        ('TRANSFERIDA', 'Transferida'),
    ]
    orden = models.OneToOneField(OrdenInternamiento, on_delete=models.CASCADE)
    cama = models.ForeignKey(Cama, on_delete=models.SET_NULL, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    signos_vitales = models.JSONField(default=dict)
    plan_medico = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_HOSP, default='ACTIVA')

    def __str__(self):
        return f"Hospitalización {self.id} - {self.orden.paciente}"

class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    hospitalizacion = models.OneToOneField(Hospitalizacion, on_delete=models.SET_NULL, null=True, blank=True)
    diagnostico = models.TextField(blank=True)
    tratamientos = models.TextField(blank=True)
    fecha_apertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HC de {self.paciente}"
