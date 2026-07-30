from django.db import models

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre