#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para generar la aplicación 'admision_hospitalizacion' 
dentro de un proyecto Django + DRF.
Ejecutar desde la raíz del proyecto (donde está manage.py).
"""

import os
import sys
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
APPS_DIR = BASE_DIR / "apps"
APP_NAME = "admision_hospitalizacion"
APP_PATH = APPS_DIR / APP_NAME

# Contenidos de los archivos a crear
FILES = {}

# __init__.py (vacío)
FILES["__init__.py"] = """# Aplicación de Admisión y Hospitalización
"""

# apps.py
FILES["apps.py"] = f"""from django.apps import AppConfig

class AdmisionHospitalizacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{APP_NAME}'
    verbose_name = 'Admisión y Hospitalización'
"""

# models.py
FILES["models.py"] = """from django.db import models
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
"""

# repositories.py
FILES["repositories.py"] = """from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

class PacienteRepository:
    @staticmethod
    def get_by_dni(dni):
        return Paciente.objects.filter(dni=dni).first()

    @staticmethod
    def create(data):
        return Paciente.objects.create(**data)

class CamaRepository:
    @staticmethod
    def find_available_by_specialty(especialidad):
        return Cama.objects.filter(especialidad=especialidad, disponible=True).first()

    @staticmethod
    def update_disponibilidad(cama, disponible):
        cama.disponible = disponible
        cama.save()
        return cama

class OrdenInternamientoRepository:
    @staticmethod
    def create(data):
        return OrdenInternamiento.objects.create(**data)

    @staticmethod
    def get_by_id(orden_id):
        return OrdenInternamiento.objects.filter(id=orden_id).first()

    @staticmethod
    def update_estado(orden, estado):
        orden.estado = estado
        orden.save()
        return orden

class HospitalizacionRepository:
    @staticmethod
    def create(data):
        return Hospitalizacion.objects.create(**data)

    @staticmethod
    def get_by_orden(orden):
        return Hospitalizacion.objects.filter(orden=orden).first()

class HistoriaClinicaRepository:
    @staticmethod
    def create(data):
        return HistoriaClinica.objects.create(**data)
"""

# services.py
FILES["services.py"] = """from django.core.exceptions import ValidationError
from .repositories import (
    PacienteRepository, CamaRepository, OrdenInternamientoRepository,
    HospitalizacionRepository, HistoriaClinicaRepository
)

class AdmisionService:

    @staticmethod
    def recepcionar_orden(data):
        paciente = PacienteRepository.get_by_dni(data['dni'])
        if not paciente:
            paciente = PacienteRepository.create({
                'dni': data['dni'],
                'nombres': data['nombres'],
                'apellidos': data['apellidos'],
                'fecha_nacimiento': data['fecha_nacimiento'],
                'telefono': data.get('telefono', '')
            })

        orden = OrdenInternamientoRepository.create({
            'paciente': paciente,
            'especialidad_solicitada': data['especialidad'],
            'medico_solicitante': data['medico_solicitante']
        })
        return orden

    @staticmethod
    def verificar_disponibilidad(orden_id):
        orden = OrdenInternamientoRepository.get_by_id(orden_id)
        if not orden:
            raise ValidationError("Orden no encontrada")

        cama = CamaRepository.find_available_by_specialty(orden.especialidad_solicitada)
        if not cama:
            OrdenInternamientoRepository.update_estado(orden, 'EN_ESPERA')
            return {'disponible': False, 'mensaje': 'No hay camas disponibles', 'orden': orden.id}
        else:
            OrdenInternamientoRepository.update_estado(orden, 'VALIDADA')
            return {'disponible': True, 'cama': cama.numero, 'orden': orden.id}

    @staticmethod
    def validar_cobertura_sis(orden_id, codigo_sis):
        # Simulación: si el código empieza con 'SIS' es válido
        if codigo_sis and codigo_sis.startswith('SIS'):
            return {'valida': True}
        else:
            orden = OrdenInternamientoRepository.get_by_id(orden_id)
            OrdenInternamientoRepository.update_estado(orden, 'RECHAZADA')
            return {'valida': False, 'mensaje': 'Cobertura SIS inválida o inactiva'}

    @staticmethod
    def iniciar_hospitalizacion(orden_id, signos_vitales):
        orden = OrdenInternamientoRepository.get_by_id(orden_id)
        if not orden or orden.estado != 'VALIDADA':
            raise ValidationError("La orden no está validada")

        cama = CamaRepository.find_available_by_specialty(orden.especialidad_solicitada)
        if not cama:
            raise ValidationError("No hay cama disponible")

        CamaRepository.update_disponibilidad(cama, False)

        hospitalizacion = HospitalizacionRepository.create({
            'orden': orden,
            'cama': cama,
            'signos_vitales': signos_vitales
        })

        HistoriaClinicaRepository.create({
            'paciente': orden.paciente,
            'hospitalizacion': hospitalizacion
        })

        orden.estado = 'FINALIZADA'
        orden.save()

        return {
            'mensaje': 'Hospitalización exitosa',
            'hospitalizacion_id': hospitalizacion.id,
            'cama': cama.numero,
            'paciente': f"{orden.paciente.nombres} {orden.paciente.apellidos}"
        }
"""

# serializers.py
FILES["serializers.py"] = """from rest_framework import serializers
from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class CamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cama
        fields = '__all__'

class OrdenInternamientoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(), source='paciente', write_only=True
    )

    class Meta:
        model = OrdenInternamiento
        fields = '__all__'

class HospitalizacionSerializer(serializers.ModelSerializer):
    orden = OrdenInternamientoSerializer(read_only=True)
    cama = CamaSerializer(read_only=True)

    class Meta:
        model = Hospitalizacion
        fields = '__all__'

class RecepcionOrdenSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    fecha_nacimiento = serializers.DateField()
    telefono = serializers.CharField(max_length=15, required=False, allow_blank=True)
    especialidad = serializers.CharField(max_length=50)
    medico_solicitante = serializers.CharField(max_length=100)

class ValidarCoberturaSerializer(serializers.Serializer):
    codigo_sis = serializers.CharField(max_length=20)

class IniciarHospitalizacionSerializer(serializers.Serializer):
    signos_vitales = serializers.JSONField()
"""

# views.py
FILES["views.py"] = """from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .services import AdmisionService
from .serializers import (
    RecepcionOrdenSerializer,
    ValidarCoberturaSerializer,
    IniciarHospitalizacionSerializer,
    OrdenInternamientoSerializer,
    HospitalizacionSerializer
)
from .models import OrdenInternamiento, Hospitalizacion

@api_view(['POST'])
def recepcionar_orden(request):
    serializer = RecepcionOrdenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        orden = AdmisionService.recepcionar_orden(serializer.validated_data)
        return Response({
            'mensaje': 'Orden recepcionada correctamente',
            'orden_id': orden.id,
            'estado': orden.estado
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def verificar_disponibilidad(request, orden_id):
    try:
        resultado = AdmisionService.verificar_disponibilidad(orden_id)
        return Response(resultado, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def validar_cobertura(request, orden_id):
    serializer = ValidarCoberturaSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = AdmisionService.validar_cobertura_sis(orden_id, serializer.validated_data['codigo_sis'])
        return Response(resultado, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def iniciar_hospitalizacion(request, orden_id):
    serializer = IniciarHospitalizacionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = AdmisionService.iniciar_hospitalizacion(
            orden_id,
            serializer.validated_data['signos_vitales']
        )
        return Response(resultado, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def listar_ordenes(request):
    ordenes = OrdenInternamiento.objects.all()
    serializer = OrdenInternamientoSerializer(ordenes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_hospitalizacion(request, hospitalizacion_id):
    try:
        hosp = Hospitalizacion.objects.get(id=hospitalizacion_id)
        serializer = HospitalizacionSerializer(hosp)
        return Response(serializer.data)
    except Hospitalizacion.DoesNotExist:
        return Response({'error': 'Hospitalización no encontrada'}, status=status.HTTP_404_NOT_FOUND)
"""

# urls.py
FILES["urls.py"] = """from django.urls import path
from . import views

urlpatterns = [
    path('api/ordenes/recepcionar/', views.recepcionar_orden, name='recepcionar_orden'),
    path('api/ordenes/<int:orden_id>/disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
    path('api/ordenes/<int:orden_id>/validar-cobertura/', views.validar_cobertura, name='validar_cobertura'),
    path('api/ordenes/<int:orden_id>/iniciar-hospitalizacion/', views.iniciar_hospitalizacion, name='iniciar_hospitalizacion'),
    path('api/ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('api/hospitalizaciones/<int:hospitalizacion_id>/', views.obtener_hospitalizacion, name='obtener_hospitalizacion'),
]
"""

# admin.py (básico)
FILES["admin.py"] = """from django.contrib import admin
from .models import Paciente, Cama, OrdenInternamiento, Hospitalizacion, HistoriaClinica

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'fecha_nacimiento')
    search_fields = ('dni', 'nombres', 'apellidos')

@admin.register(Cama)
class CamaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'especialidad', 'disponible')
    list_filter = ('disponible', 'especialidad')

@admin.register(OrdenInternamiento)
class OrdenInternamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'especialidad_solicitada', 'estado', 'fecha_emision')
    list_filter = ('estado', 'especialidad_solicitada')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'medico_solicitante')

@admin.register(Hospitalizacion)
class HospitalizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'cama', 'fecha_ingreso', 'estado')
    list_filter = ('estado',)

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'hospitalizacion', 'fecha_apertura')
    search_fields = ('paciente__nombres', 'paciente__apellidos')
"""

# tests.py (básico)
FILES["tests.py"] = """from django.test import TestCase
from .models import Paciente, Cama, OrdenInternamiento

class ModelTests(TestCase):
    def test_paciente_creation(self):
        paciente = Paciente.objects.create(
            dni='12345678',
            nombres='Juan',
            apellidos='Perez',
            fecha_nacimiento='1980-01-01'
        )
        self.assertEqual(paciente.nombres, 'Juan')
        self.assertEqual(str(paciente), 'Juan Perez')

    def test_cama_disponible(self):
        cama = Cama.objects.create(numero='101', especialidad='Medicina Interna')
        self.assertTrue(cama.disponible)
        self.assertEqual(str(cama), 'Cama 101 - Medicina Interna')
"""


def create_app():
    # Crear directorio de la aplicación
    if APP_PATH.exists():
        print(f"⚠️  La carpeta {APP_PATH} ya existe. Se sobrescribirán los archivos.")
    else:
        APP_PATH.mkdir(parents=True, exist_ok=True)
        print(f"✅ Carpeta creada: {APP_PATH}")

    # Escribir archivos
    for filename, content in FILES.items():
        filepath = APP_PATH / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 Creado: {filepath}")

    # Actualizar el urls.py principal
    main_urls = BASE_DIR / "HospitalDjangoAPI" / "urls.py"
    if main_urls.exists():
        with open(main_urls, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar si ya existe la inclusión
        include_line = f"path('', include('apps.{APP_NAME}.urls')),"
        if include_line not in content:
            # Buscar el lugar adecuado (después de admin o al final de urlpatterns)
            if 'urlpatterns = [' in content:
                # Insertar antes del corchete de cierre
                lines = content.splitlines()
                new_lines = []
                inserted = False
                for line in lines:
                    new_lines.append(line)
                    if 'urlpatterns = [' in line and not inserted:
                        # Añadir la nueva línea después de la apertura
                        new_lines.append(f"    {include_line}")
                        inserted = True
                if not inserted:
                    # Si no se encontró, añadir al final
                    new_lines.append(f"urlpatterns += [\n    path('', include('apps.{APP_NAME}.urls')),\n]")
                new_content = "\n".join(new_lines)
                # También asegurarse de importar include si no está
                if 'from django.urls import include' not in new_content:
                    new_content = new_content.replace(
                        'from django.urls import path',
                        'from django.urls import path, include'
                    )
                with open(main_urls, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Actualizado {main_urls} con la inclusión de rutas.")
            else:
                print("⚠️  No se pudo actualizar automáticamente el urls.py. Debes agregar manualmente:")
                print(f"   path('', include('apps.{APP_NAME}.urls')),")
        else:
            print("ℹ️  La inclusión de rutas ya existe en urls.py.")
    else:
        print(f"⚠️  No se encontró el archivo {main_urls}. Debes agregar manualmente la inclusión de rutas.")

    # Mensajes finales
    print("\n" + "="*50)
    print("✅ Generación completada.")
    print("Ahora ejecuta los siguientes comandos:")
    print(f"   1. python manage.py makemigrations {APP_NAME}")
    print("   2. python manage.py migrate")
    print("   3. python manage.py createsuperuser  (opcional, para acceder al admin)")
    print("   4. python manage.py runserver")
    print("\nRecuerda agregar datos de prueba (camas) desde el admin o mediante fixtures.")
    print("="*50)


if __name__ == "__main__":
    # Verificar que estamos en el directorio correcto
    if not (BASE_DIR / "manage.py").exists():
        print("❌ Error: No se encontró manage.py. Asegúrate de ejecutar el script desde la raíz del proyecto.")
        sys.exit(1)
    create_app()