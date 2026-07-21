from django.db import models


class EquipoBio(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=200)
    modelo = models.CharField(max_length=100)
    num_serie = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    fecha_adq = models.DateField(null=True, blank=True, db_column='fecha_adquisicion')
    fecha_ult_calib = models.DateField(null=True, blank=True, db_column='fecha_ultima_calibracion')
    estado = models.CharField(max_length=30, default='OPER')

    class Meta:
        db_table = 'mb_equipo_biomedico'
        verbose_name = 'Equipo Biomedico'
        verbose_name_plural = 'Equipos Biomedicos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
