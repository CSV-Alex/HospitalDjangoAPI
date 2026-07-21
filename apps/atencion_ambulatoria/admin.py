from django.contrib import admin
from .models import Paciente, Cita, Triaje, HistoriaClinica, PeticionPrueba

admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Triaje)
admin.site.register(HistoriaClinica)
admin.site.register(PeticionPrueba)