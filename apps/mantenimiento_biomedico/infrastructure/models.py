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


class Reporte(models.Model):
    equipo = models.ForeignKey(EquipoBio, on_delete=models.CASCADE, related_name='reportes')
    descripcion = models.TextField()
    reportado_por = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha_reporte')
    estado = models.CharField(max_length=30, default='PEND')

    class Meta:
        db_table = 'mb_reporte_equipo'
        verbose_name = 'Reporte de Equipo'
        verbose_name_plural = 'Reportes de Equipos'

    def __str__(self):
        return f"Reporte #{self.id} - {self.equipo.nombre}"


class Eval(models.Model):
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='evaluaciones')
    tecnico = models.CharField(max_length=200)
    diagnostico = models.TextField()
    reemplazo = models.BooleanField(default=False, db_column='requiere_reemplazo')
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha_evaluacion')

    class Meta:
        db_table = 'mb_evaluacion_tecnica'
        verbose_name = 'Evaluacion Tecnica'
        verbose_name_plural = 'Evaluaciones Tecnicas'

    def __str__(self):
        return f"Eval #{self.id} - Reporte #{self.reporte_id}"


class Solicitud(models.Model):
    eval = models.ForeignKey(Eval, on_delete=models.CASCADE, related_name='solicitudes', db_column='evaluacion_id')
    equipo = models.ForeignKey(EquipoBio, on_delete=models.CASCADE, related_name='solicitudes_reemplazo')
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha_solicitud')
    estado = models.CharField(max_length=30, default='PEND')

    class Meta:
        db_table = 'mb_solicitud_reemplazo'
        verbose_name = 'Solicitud de Reemplazo'
        verbose_name_plural = 'Solicitudes de Reemplazo'

    def __str__(self):
        return f"Solicitud #{self.id} - Equipo {self.equipo.nombre}"


class Estimacion(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='estimaciones')
    precio = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio_estimado')
    proveedor = models.CharField(max_length=200)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha_estimacion')

    class Meta:
        db_table = 'mb_estimacion_precios'
        verbose_name = 'Estimacion de Precios'
        verbose_name_plural = 'Estimaciones de Precios'

    def __str__(self):
        return f"Estimacion #{self.id} - {self.proveedor}"


class Interv(models.Model):
    equipo = models.ForeignKey(EquipoBio, on_delete=models.CASCADE, related_name='intervenciones')
    solicitud = models.ForeignKey(Reporte, on_delete=models.SET_NULL, null=True, blank=True, related_name='intervenciones')
    tipo = models.CharField(max_length=30)
    descripcion = models.TextField()
    tecnico = models.CharField(max_length=200, db_column='tecnico_responsable')
    fecha_ini = models.DateTimeField(auto_now_add=True, db_column='fecha_inicio')
    fecha_fin = models.DateTimeField(null=True, blank=True)
    resultado = models.TextField(null=True, blank=True)
    obs = models.TextField(null=True, blank=True, db_column='observaciones')

    class Meta:
        db_table = 'mb_intervencion'
        verbose_name = 'Intervencion'
        verbose_name_plural = 'Intervenciones'

    def __str__(self):
        return f"Interv #{self.id} - {self.equipo.nombre} ({self.tipo})"
