from django.db import models

class Paciente(models.Model):
    
    numero_historia_clinica = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        help_text="Número único de historia clínica"
    )
    
    dni = models.CharField(
        max_length=8,
        unique=False,
        null=True,
        blank=True,
        help_text="Documento de identidad del paciente"
    )
    
    nombre_completo = models.CharField(
        max_length=255,
        null=False,
        help_text="Nombre completo del paciente"
    )
    
    fecha_nacimiento = models.DateField(
        null=False,
        help_text="Fecha de nacimiento del paciente"
    )
    
    necesita_examen = models.BooleanField(
        default=False,
        help_text="El paciente necesita examen de laboratorio?"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última actualización"
    )

    class Meta:
        app_label = 'consultorio_externo'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_historia_clinica']),
            models.Index(fields=['dni']),
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.numero_historia_clinica})"


class Cita(models.Model):
    """Modelo para gestionar citas de consultorios externos."""
    
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

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='citas',
        help_text="Referencia al paciente"
    )
    
    fecha_hora = models.DateTimeField(
        help_text="Fecha y hora de la cita"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PROGRAMADA,
        help_text="Estado actual de la cita"
    )

    class Meta:
        app_label = 'consultorio_externo'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['paciente', 'fecha_hora']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"Cita de {self.paciente.nombre_completo} - {self.fecha_hora}"


class Triaje(models.Model):
    """Modelo para registrar el triaje de pacientes."""
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='triajes',
        help_text="Referencia al paciente"
    )
    
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora del triaje"
    )
    
    presion_sistolica = models.IntegerField(
        help_text="Presión sistólica (mmHg)"
    )
    
    presion_diastolica = models.IntegerField(
        help_text="Presión diastólica (mmHg)"
    )
    
    temperatura = models.FloatField(
        help_text="Temperatura corporal (°C)"
    )

    class Meta:
        app_label = 'consultorio_externo'
        verbose_name = 'Triaje'
        verbose_name_plural = 'Triajes'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['paciente', 'fecha_hora']),
        ]

    def __str__(self):
        return f"Triaje de {self.paciente.nombre_completo} - {self.fecha_hora}"


class HistoriaClinica(models.Model):
    
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='historia_clinica',
        help_text="Referencia al paciente"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la historia clínica"
    )
    
    diagnostico = models.TextField(
        blank=True,
        null=True,
        help_text="Diagnóstico del paciente"
    )
    
    tratamiento = models.TextField(
        blank=True,
        null=True,
        help_text="Tratamiento recomendado"
    )
    
    receta_medica = models.TextField(
        blank=True,
        null=True,
        help_text="Receta médica prescrita"
    )

    class Meta:
        app_label = 'consultorio_externo'
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historia clínica de {self.paciente.nombre_completo}"


class PeticionPrueba(models.Model):
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='peticiones_prueba',
        help_text="Referencia al paciente"
    )
    
    tipo_examen = models.CharField(
        max_length=255,
        help_text="Tipo de examen solicitado"
    )
    
    tiene_sis = models.BooleanField(
        default=False,
        help_text="El examen está cubierto por el SIS?"
    )
    
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de solicitud del examen"
    )

    class Meta:
        app_label = 'consultorio_externo'
        verbose_name = 'Petición de Prueba'
        verbose_name_plural = 'Peticiones de Prueba'
        ordering = ['-fecha_solicitud']
        indexes = [
            models.Index(fields=['paciente', 'fecha_solicitud']),
        ]

    def __str__(self):
        return f"Petición: {self.tipo_examen} - {self.paciente.nombre_completo}"